"""
Provides an SGr-specific implementation that transforms JSON data using JMESpath mappings.
"""

import collections
import json
import re
import copy
from typing import Any, Optional
import jmespath
from sgr_specification.v0.generic.base_types import (
    JmespathMappingRecord
)


class RecordKey(object):
    """
    Implements a key with indices. Ported from Java.
    """

    def __init__(self):
        self._indices: list[str] = list()

    def add(self, idx: int):
        self._indices.append(str(idx))

    def index(self, iteration: int) -> int:
        return int(self._indices[iteration])

    def key(self) -> str:
        return str.join('', self._indices)

    def __eq__(self, other):
        if not isinstance(other, RecordKey):
            return False
        if self._indices == other._indices:
            return True
        if len(self._indices) != len(other._indices):
            return False
        for idx in range(0, len(self._indices)):
            if self._indices[idx] != other._indices[idx]:
                return False
        return True

    def __hash__(self):
        return hash(self.key())

    def __str__(self) -> str:
        return self.key()

    def __repr__(self) -> str:
        return f'<RecordKey={self.key()}>'


def map_json_response(response: str, mappings: list[JmespathMappingRecord]) -> str:
    """
    Converts the structure of a JSON string using JMESpath mappings.

    Parameters
    ----------
    response : str
        the JSON string to convert
    mappings : list[JmespathMappingRecord]
        the data point's configured mappings

    Returns
    -------
    str
        the mapped JSON string
    """

    if len(mappings) == 0:
        return response

    # Build mapping tables from EI-XML mappings
    map_from: dict[str, str] = collections.OrderedDict()
    map_to: dict[str, str] = collections.OrderedDict()
    names: dict[str, str] = collections.OrderedDict()

    for i, m in enumerate(mappings):
        if m.from_value and m.to:
            map_from[str(i)] = m.from_value
            if m.from_value.startswith('$'):
                map_to[m.from_value] = m.to
            else:
                map_to[str(i)] = m.to
        if m.name is not None:
            names[str(i)] = m.name

    flat_representation = _map_to_flat_list(response, map_from)
    if flat_representation is None:
        raise ValueError("unable to flatten JSON response")

    enhanced_map = _enhance_with_namings(flat_representation, names)

    return json.dumps(_build_json_node(map_to, list(enhanced_map.values())))


def _map_to_flat_list(json_str: str, keyword_map: dict[str, str]) -> Optional[dict[RecordKey, dict[str, Any]]]:
    root = json.loads(json_str)
    return _parse_json_tree(root, None, 1, keyword_map)


def _enhance_with_namings(flat_representation: dict[RecordKey, dict[str, Any]], names: dict[str, str]) -> dict[int, dict[str, Any]]:
    enhanced: dict[int, dict[str, Any]] = collections.OrderedDict()
    key = 0
    for (vk, vm) in flat_representation.items():
        for i in range(0, len(vm)):
            if len(names) != 0:
                (fk, fr) = _flatten_named_records(key, vm, names)
                enhanced.update(fr)
                key = fk
            else:
                enhanced[key] = vm
                key = key + 1
    return enhanced


def _flatten_named_records(cur_key: int, values: dict[str, Any], names: dict[str, str]) -> tuple[int, dict[int, dict[str, Any]]]:
    flat_records: dict[int, dict[str, Any]] = collections.OrderedDict()
    unnamed_values: dict[str, Any] = collections.OrderedDict()

    for (k, v) in values.items():
        if k not in names:
            unnamed_values[k] = v

    for (k, v) in names.items():
        # Create a separate record for each name
        new_values = copy.deepcopy(unnamed_values)
        new_values[v] = v.replace('$', '')
        new_values[k] = values[k]
        flat_records[cur_key] = new_values
        cur_key = cur_key + 1

    return (cur_key, flat_records)


def _parse_json_tree(node: Any, parent_data: Optional[dict[RecordKey, dict[str, Any]]], iteration: int, keyword_map: dict[str, str]) -> Optional[dict[RecordKey, dict[str, Any]]]:
    # preserves element order
    record_map: dict[RecordKey, dict[str, Any]] = collections.OrderedDict()

    keywords = _get_keywords_for_iteration(iteration, keyword_map)

    if iteration <= _determine_required_iterations(keyword_map):
        if not parent_data:
            _process_child_elements(node, iteration, record_map, keywords, 0, None)
        else:
            parent_idx = 0
            for parent_rec in parent_data.items():
                _process_child_elements(node, iteration, record_map, keywords, parent_idx, parent_rec)
                parent_idx = parent_idx + 1
        return _parse_json_tree(node, record_map, iteration + 1, keyword_map)

    return parent_data


def _get_keywords_for_iteration(iteration: int, keyword_map: dict[str, str]) -> list[tuple[str, str]]:
    return list(filter(lambda item: item[1].count('[*]') == iteration, keyword_map.items()))


def _determine_required_iterations(keyword_map: dict[str, str]) -> int:
    max = 0
    for v in keyword_map.values():
        i = v.count('[*]')
        if i > max:
            max = i
    return max


def _get_number_of_elements(node: Any, parent_idx: int, keyword: tuple[str, str], iteration: int) -> int:
    pattern = keyword[1]
    regex = re.compile('\\[\\*\\]')
    for i in range(1, iteration):
        pattern = re.sub(regex, f'[{parent_idx}]', keyword[1], 1)
    expr = jmespath.compile(f'{pattern} | length(@)')
    result = expr.search(node, jmespath.Options(dict_cls=collections.OrderedDict))
    return int(result)


def _process_child_elements(
        node: Any,
        iteration: int,
        record_map: dict[RecordKey, dict[str, Any]],
        keywords: list[tuple[str, str]],
        parent_idx: int, parent_rec: Optional[tuple[RecordKey, dict[str, Any]]]
):
    if len(keywords) > 0:
        kw = keywords[0]
        n_elem = _get_number_of_elements(node, parent_idx, kw, iteration)
        for i in range(0, n_elem):
            key = copy.deepcopy(parent_rec[0]) if parent_rec else RecordKey()
            key.add(i)
            if parent_rec is None:
                # process root node
                record_map[key] = collections.OrderedDict()
            else:
                # process the child nodes, mix-in the values of the parent node
                record_map[key] = copy.deepcopy(parent_rec[1])

            for kw in keywords:
                _add_child_element(node, record_map, key, kw, iteration)


def _add_child_element(node: Any, record_map: dict[RecordKey, dict[str, Any]], key: RecordKey, kw: tuple[str, str], iteration: int):
    pattern = kw[1]
    regex = re.compile('\\[\\*\\]')
    for i in range(0, iteration):
        pattern = re.sub(regex, f'[{key.index(i)}]', pattern, 1)
    node_val = jmespath.search(pattern, node)
    if isinstance(node_val, str):
        record_map[key][kw[0]] = str(node_val)
    if isinstance(node_val, float):
        record_map[key][kw[0]] = float(node_val)
    if isinstance(node_val, int):
        record_map[key][kw[0]] = int(node_val)


def _get_first_level_elements(keywords: list[tuple[str, str]]) -> dict[str, str]:
    result: dict[str, str] = collections.OrderedDict()
    regex = re.compile('\\[\\*\\]\\.(.*?)$')
    for kw in keywords:
        rs = regex.match(kw[1])
        if rs is not None:
            target_name = rs.group(1)
            result[kw[0]] = target_name
    return result


def _get_second_level_elements(keywords: list[tuple[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = collections.OrderedDict()
    regex = re.compile('\\[\\*\\]\\.(.*?)\\[\\*\\]')
    for kw in keywords:
        rs = regex.match(kw[1])
        if rs is not None:
            group_key = rs.group(1)
            value_names: dict[str, str] = result[group_key] if group_key in result else collections.OrderedDict()
            value_name = re.sub('\\[\\*\\]\\.(.*?)\\[\\*\\]\\.', '', kw[1])
            value_names[kw[0]] = value_name
            result[group_key] = value_names
    return result


def _add_second_level_nodes(first_level_node: dict, flat_records_belonging_to_group: list[dict[str, Any]], keyword_map: dict[str, str]):
    keywords_for_iteration = _get_keywords_for_iteration(2, keyword_map)
    second_level_groups: dict[str, list[dict[str, Any]]] = collections.OrderedDict()

    for frg in flat_records_belonging_to_group:
        # build combined key
        ck = ''
        for ki in keywords_for_iteration:
            ck = ck + str(frg[ki[0]])
        # get the group by the combined key or add a new group if it does not exist
        record_group = second_level_groups[ck] if ck in second_level_groups else list()
        record_group.append(frg)
        second_level_groups[ck] = record_group

    second_level_group_elements = _get_second_level_elements(keywords_for_iteration)
    for (parent_name, child_name_mapping) in second_level_group_elements.items():
        array_node: list[Any] = list()
        first_level_node[parent_name] = array_node
        for (group_key, flat_records_of_group) in second_level_groups.items():
            object_node = collections.OrderedDict()
            for flat_record in flat_records_of_group:
                for (value_names, values) in flat_record.items():
                    for mapping_entry in keywords_for_iteration:
                        val = flat_record[mapping_entry[0]]
                        if isinstance(val, float):
                            object_node[child_name_mapping[mapping_entry[0]]] = float(val)
                        elif isinstance(val, int):
                            object_node[child_name_mapping[mapping_entry[0]]] = int(val)
                        elif val is not None:
                            object_node[child_name_mapping[mapping_entry[0]]] = str(val)
            array_node.append(object_node)


def _build_json_node(keyword_map: dict[str, str], flat_data_records: list[dict[str, Any]]) -> Any:
    # group by first level group
    keywords_for_iteration = _get_keywords_for_iteration(1, keyword_map)
    # put all records that have the same first level values into one group with a combined key, built from the values.
    first_level_groups: dict[str, list[dict[str, Any]]] = collections.OrderedDict()

    for fr in flat_data_records:
        # build combined key
        ck = ''
        for ki in keywords_for_iteration:
            ck = ck + str(fr[ki[0]])
        # get the group by the combined key or add a new group if it does not exist
        record_group = first_level_groups[ck] if ck in first_level_groups else list()
        # add the flat to the group it belongs to
        record_group.append(fr)
        # update first level group map
        first_level_groups[ck] = record_group

    # get a mapping for the source element names to the destination element names
    first_level_name_mappings = _get_first_level_elements(keywords_for_iteration)

    # build the json node, assume the root node is an array
    root_node: list[Any] = []

    for (group_key, flat_records_belonging_to_group) in first_level_groups.items():
        # add a node for each group to the array node
        first_level_node = collections.OrderedDict()
        for frg in flat_records_belonging_to_group:
            for (names, values) in frg.items():
                # pick all first level elements, map the elementNames get the values and add the elements to the  firstLevel node
                for mapping_entry in keywords_for_iteration:
                    val = frg[mapping_entry[0]]
                    if isinstance(val, float):
                        first_level_node[first_level_name_mappings[mapping_entry[0]]] = float(val)
                    elif isinstance(val, int):
                        first_level_node[first_level_name_mappings[mapping_entry[0]]] = int(val)
                    elif val is not None:
                        first_level_node[first_level_name_mappings[mapping_entry[0]]] = str(val)
            # then add the second level nodes to the first level node
            _add_second_level_nodes(first_level_node, flat_records_belonging_to_group, keyword_map)
        # we have finished adding the first level node
        root_node.append(first_level_node)

    return root_node

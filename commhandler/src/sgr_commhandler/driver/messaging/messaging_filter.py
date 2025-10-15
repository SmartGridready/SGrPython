"""
Provides message filter implementations.
"""

import re
import json
import jmespath
from typing import Any, Generic, Optional, TypeVar

from sgr_specification.v0.generic.base_types import (
    JmespathFilterType,
    PlaintextFilterType,
    RegexFilterType
)
from sgr_specification.v0.product.messaging_types import MessageFilter


T = TypeVar('T')


class MessagingFilter(Generic[T]):
    """
    The base class for message filter implementations.
    """

    def __init__(self, filter_spec: T):
        self._filter_spec = filter_spec

    def is_filter_match(self, payload: Any) -> bool:
        ...


class JMESPathMessagingFilter(MessagingFilter[JmespathFilterType]):
    """
    Implements a JMESpath filter for message payloads.
    """

    def __init__(self, filter_spec: JmespathFilterType):
        super(JMESPathMessagingFilter, self).__init__(filter_spec)

    def is_filter_match(self, payload: Any) -> bool:
        ret_value = str(payload)
        regex = self._filter_spec.matches_regex or '.'
        if self._filter_spec.query:
            ret_value = json.dumps(jmespath.search(self._filter_spec.query, json.loads(payload)))

        match = re.match(regex, ret_value)
        return match is not None


class PlaintextMessagingFilter(MessagingFilter[PlaintextFilterType]):
    """
    Implements a plain text filter for message payloads.
    """

    def __init__(self, filter_spec: PlaintextFilterType):
        super(PlaintextMessagingFilter, self).__init__(filter_spec)

    def is_filter_match(self, payload: Any) -> bool:
        ret_value = str(payload)
        regex = self._filter_spec.matches_regex or '.'

        match = re.match(regex, ret_value)
        return match is not None


class RegexMessagingFilter(MessagingFilter[RegexFilterType]):
    """
    Implements a regex filter for message payloads.
    """

    def __init__(self, filter_spec: RegexFilterType):
        super(RegexMessagingFilter, self).__init__(filter_spec)

    def is_filter_match(self, payload: Any) -> bool:
        ret_value = str(payload)
        regex = self._filter_spec.matches_regex or '.'
        if self._filter_spec.query:
            query_match = re.match(self._filter_spec.query, ret_value)
            if query_match is not None:
                ret_value = query_match.group()

        match = re.match(regex, ret_value)
        return match is not None


def get_messaging_filter(filter: MessageFilter) -> Optional[MessagingFilter]:
    """
    Creates a messaging filter from specification.

    Parameters
    ----------
    filter : MessageFilter
        the filter specification

    Returns
    -------
    Optional[MessagingFilter]
        the messaging filter, if it could be created
    """

    if filter.jmespath_filter:
        return JMESPathMessagingFilter(filter.jmespath_filter)
    elif filter.plaintext_filter:
        return PlaintextMessagingFilter(filter.plaintext_filter)
    elif filter.regex_filter:
        raise Exception('regexFilter not supported')
    elif filter.xpapath_filter:
        raise Exception('xpapathFilter not supported')
    return None

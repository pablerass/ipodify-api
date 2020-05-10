# -*- coding: utf-8 -*-
import pytest

from ipodify_api.model.track import TrackPropertyFilter


@pytest.fixture
def basic_filter():
    return TrackPropertyFilter("$eq", "artists", "Eiffel 65")
"""Tests for independently maintainable experiment variants."""


def test_result_and_source_are_independent(make_variant):
    source = {"seed": 7, "sample_sizes": [10, 20, 30]}
    expected_source = {"seed": 7, "sample_sizes": [10, 20, 30]}
    expected_result = {"seed": 9, "sample_sizes": [10, 25, 30]}

    result = make_variant(source, seed=9, index=1, replacement=25)

    assert result == expected_result
    assert result is not source
    assert result["sample_sizes"] is not source["sample_sizes"]
    assert source == expected_source


def test_later_changes_to_result_do_not_change_source(make_variant):
    source = {"seed": 7, "sample_sizes": [10, 20, 30]}
    expected_source = {"seed": 7, "sample_sizes": [10, 20, 30]}

    result = make_variant(source, seed=9, index=1, replacement=25)
    result["seed"] = 11
    result["sample_sizes"][0] = 15

    assert source == expected_source


def test_repeated_calls_produce_independent_results(make_variant):
    source = {"seed": 7, "sample_sizes": [10, 20, 30]}
    expected_source = {"seed": 7, "sample_sizes": [10, 20, 30]}
    expected_result = {"seed": 9, "sample_sizes": [10, 25, 30]}

    first = make_variant(source, seed=9, index=1, replacement=25)
    second = make_variant(source, seed=9, index=1, replacement=25)

    assert first == expected_result
    assert second == expected_result
    assert first == second
    assert first is not second
    assert first["sample_sizes"] is not second["sample_sizes"]

    first["seed"] = 11
    first["sample_sizes"][0] = 15
    assert second == expected_result
    assert source == expected_source

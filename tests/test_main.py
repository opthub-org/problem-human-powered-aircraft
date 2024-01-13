# SHOULD implement test cases
# 長いので複数ファイルに分割を検討

import jsonschema
from click.testing import CliRunner

import problem_awesome_problem.main as main
from conftest import *


###############################
# ここからvalidate_inputのテスト #
###############################

# 意味のない入力に対してはValidationErrorを送出する．
def test_validate_input_nonsense_input(nonsense_input, schema):
    with pytest.raises(jsonschema.ValidationError):
        main.validate_input(nonsense_input, schema)


# スキーマに適合した入力に対しては何も起きない．
# 特に境界値付近は必ず検証すること．
def test_validate_input_valid_input():
    try:
        main.validate_input({}, {})
    except Exception as e:
        pytest.fail(str(e))


# 入力がオブジェクト/ディクショナリの場合は，無関係のフィールド/キーを許容しない
def test_validate_input_extra_key():
    valid_input = {}
    # valid_input["extra_key"] = "hoge"
    with pytest.raises(jsonschema.ValidationError):
        main.validate_input(valid_input, {})


# 入力がオブジェクト/ディクショナリの場合は，必須のフィール/キーを検証する．
def test_validate_input_must_key():
    valid_input = {}
    # valid_input.pop("must_key")
    with pytest.raises(jsonschema.ValidationError):
        main.validate_input(valid_input, {})


# 入力の型をチェックする．
def test_validate_input_input_type():
    invalid_input = {}
    with pytest.raises(jsonschema.ValidationError):
        main.validate_input(invalid_input, {})


# 範囲外の入力に対してはValidationErrorを送出する．
# 特に境界値付近は必ず検証すること．
def test_validate_input_out_of_range():
    pass


# 入力にNaNを含むケース．
def test_validate_input_nan_input(nan_input, schema):
    pass


# 入力にnullを含むケース．
def test_validate_input_null_input(null_input, schema):
    pass


# 入力にinfを含むケース．
def test_validate_input_inf_input(inf_input, schema):
    pass


# 入力に-infを含むケース．
def test_validate_input_minf_input(minf_input, schema):
    pass


###############################
# ここまでvalidate_inputのテスト #
###############################

################################
# ここからcalc_evaluationのテスト #
################################

# 期待される計算結果になるか検証する．
# 特に境界値付近は必ず検証すること．
def test_calc_evaluation_valid_input():
    pass


# 入力にNaNを含むケース
def test_calc_evaluation_nan_input(nan_input):
    out_obj = main.calc_evaluation(nan_input)
    assert out_obj == [1, 2, 3, 4]


# 入力にnullを含むケース
def test_calc_evaluation_null_input(null_input):
    out_obj = main.calc_evaluation(null_input)
    assert out_obj == [1, 2, 3, 4]


# 入力にinfを含むケース
def test_calc_evaluation_inf_input(inf_input):
    out_obj = main.calc_evaluation(inf_input)
    assert out_obj == [1, 2, 3, 4]


# 入力に-infを含むケース
def test_calc_evaluation_minf_input(minf_input):
    out_obj = main.calc_evaluation(minf_input)
    assert out_obj == [1, 2, 3, 4]


################################
# ここまでcalc_evaluationのテスト #
################################

##############################
# ここからformat_outputのテスト #
##############################

# 必須のキーをチェック
@pytest.mark.skip
def must_keys(formatted):
    assert "objetive" in formatted
    assert "constraint" in formatted
    assert "error" in formatted
    assert "info" in formatted


# 異常終了時の値をチェック
@pytest.mark.skip
def finish_on_error(formatted):
    assert formatted["objetive"] is None
    assert formatted["constraint"] is None
    assert type(formatted["error"]) is str
    assert formatted["info"] is None


# 期待される整形結果になるか検証する
def test_format_output_valid_input():
    valid_input = {}
    formatted = main.format_output(valid_input)

    # 必須のキー
    must_keys(formatted)

    assert formatted["objetive"] == [1, 2, 3, 4]


# 計算結果にNaNを含むケース
def test_format_output_nan_input(nan_input):
    formatted = main.format_output(nan_input)

    # 必須のキー
    must_keys(formatted)

    assert formatted["objetive"] == [1, 2, 3, 4]


# 計算結果にnullを含むケース
def test_format_output_null_input(null_input):
    formatted = main.format_output(null_input)

    # 必須のキー
    must_keys(formatted)

    assert formatted["objetive"] == [1, 2, 3, 4]


# 計算結果にinfを含むケース
def test_format_output_inf_input(inf_input):
    formatted = main.format_output(inf_input)

    # 必須のキー
    must_keys(formatted)

    assert formatted["objetive"] == [1, 2, 3, 4]


# 計算結果に-infを含むケース
def test_format_output_minf_input(minf_input):
    formatted = main.format_output(minf_input)

    # 必須のキー
    must_keys(formatted)

    assert formatted["objetive"] == [1, 2, 3, 4]


# エラーコード代わりに特別な値を返すケース
# 値を返す場合
def test_format_output_on_error():
    formatted = main.format_output(float('nan'))

    # 必須のキー
    must_keys(formatted)

    # 異常終了時の値
    finish_on_error(formatted)


# エラーコード代わりに特別な値を返すケース
# 例外スローする場合
def test_format_output_on_error2():
    with pytest.raises(Exception):
        main.format_output(float('nan'))


##############################
# ここまでformat_outputのテスト #
##############################

#########################
# ここからevaluateのテスト #
#########################

# 期待される計算結果になるか検証する．
# 特に境界値付近は必ず検証すること．
def test_evaluate_valid_input():
    pass


# 入力にNaNを含むケース．
def test_evaluate_nan_input(nan_input):
    pass


# 入力にnullを含むケース．
def test_evaluate_null_input(null_input):
    pass


# 入力にinfを含むケース．
def test_evaluate_inf_input(inf_input):
    pass


# 入力に-infを含むケース．
def test_evaluate_minf_input(minf_input):
    pass


#########################
# ここまでevaluateのテスト #
#########################

#####################
# ここからmainのテスト #
#####################

# 正常でないJSON文字列にはJSONDecodeErrorを送出する．
def test_main_invalid_json_string(invalid_json_string):
    runner = CliRunner()
    with pytest.raises(json.decoder.JSONDecodeError):
        runner.invoke(main.main, input=invalid_json_string, catch_exceptions=False)


# 期待される計算結果になるか検証する．
# 特に境界値付近は必ず検証すること．
def test_main_valid_json_string(capfd):
    valid_json_string = ""
    runner = CliRunner()
    runner.invoke(main.main, input=valid_json_string, catch_exceptions=False)
    captured = capfd.readouterr()
    assert captured.out == json.dumps(json.loads("""
        {
            "objective": [1,2,3,4],
            "constraint": null,
            "error": null,
            "info": {
                "something": "message"
            }
        }
    """)) + "\n"


# 入力にNaNを含むケース．
def test_main_nan_json_string(capfd, nan_json_string):
    runner = CliRunner()
    runner.invoke(main.main, input=nan_json_string, catch_exceptions=False)
    captured = capfd.readouterr()
    assert captured.out == json.dumps(json.loads("""
        {
            "objective": [1,2,3,4],
            "constraint": null,
            "error": null,
            "info": {
                "something": "message"
            }
        }
    """)) + "\n"


# 入力にnullを含むケース．
def test_main_null_json_string(capfd, null_json_string):
    runner = CliRunner()
    runner.invoke(main.main, input=null_json_string, catch_exceptions=False)
    captured = capfd.readouterr()
    assert captured.out == json.dumps(json.loads("""
        {
            "objective": [1,2,3,4],
            "constraint": null,
            "error": null,
            "info": {
                "something": "message"
            }
        }
    """)) + "\n"


# 入力にinfを含むケース．
def test_main_inf_json_string(capfd, inf_json_string):
    runner = CliRunner()
    runner.invoke(main.main, input=inf_json_string, catch_exceptions=False)
    captured = capfd.readouterr()
    assert captured.out == json.dumps(json.loads("""
        {
            "objective": [1,2,3,4],
            "constraint": null,
            "error": null,
            "info": {
                "something": "message"
            }
        }
    """)) + "\n"


# 入力に-infを含むケース．
def test_main_minf_json_string(capfd, minf_json_string):
    runner = CliRunner()
    runner.invoke(main.main, input=minf_json_string, catch_exceptions=False)
    captured = capfd.readouterr()
    assert captured.out == json.dumps(json.loads("""
        {
            "objective": [1,2,3,4],
            "constraint": null,
            "error": null,
            "info": {
                "something": "message"
            }
        }
    """)) + "\n"

#####################
# ここまでmainのテスト #
#####################

from flask import Flask, render_template_string
import flask_featureflags as feature_flags

FEATURE_NAME = u"test_feature"

FEATURE_IS_ON = 'OK'
FEATURE_IS_OFF = "flag is off"

def NullFlagHandler(feature):
  """ This handler always returns False """
  return False

def AlwaysOffFlagHandler(feature):
  """ This handler always returns False and halts any further checking. """
  raise feature_flags.StopCheckingFeatureFlags

def AlwaysOnFlagHandler(feature):
  """ This handler always returns True """
  return True

# This is a toy app that demos the features we're trying to test.

app = Flask(__name__)

feature_setup = feature_flags.FeatureFlag(app)

@app.route("/null")
def redirect_destination():
  return FEATURE_IS_ON

@app.route("/decorator")
@feature_flags.is_active_feature(FEATURE_NAME)
def feature_decorator():
  return FEATURE_IS_ON

@app.route("/redirect")
@feature_flags.is_active_feature(FEATURE_NAME, redirect_to='/null')
def redirect_with_decorator():
  return FEATURE_IS_ON

@app.route("/view")
def view_based_feature_flag():
  if feature_flags.is_active("test_feature"):
    return FEATURE_IS_ON
  else:
    return FEATURE_IS_OFF

@app.route("/template")
def template_based_feature_flag():
  template_string = """
    {% if 'test_feature' is active_feature %}
      OK
    {% else %}
      flag is off
    {% endif %}"""

  return render_template_string(template_string)
(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['check.tmpl'] = template(function (Handlebars,depth0,helpers,partials,data) {
  helpers = helpers || Handlebars.helpers;
  var buffer = "", stack1, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, functionType="function", self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1, foundHelper;
  buffer += "\n    <button ";
  stack1 = {};
  stack1['target'] = "entries";
  foundHelper = helpers.action;
  stack1 = foundHelper ? foundHelper.call(depth0, "clearCompleted", {hash:stack1}) : helperMissing.call(depth0, "action", "clearCompleted", {hash:stack1});
  buffer += escapeExpression(stack1) + " ";
  stack1 = {};
  stack1['class'] = "buttonClass:hidden";
  foundHelper = helpers.bindAttr;
  stack1 = foundHelper ? foundHelper.call(depth0, {hash:stack1}) : helperMissing.call(depth0, "bindAttr", {hash:stack1});
  buffer += escapeExpression(stack1) + " >\n      Clear completed (";
  stack1 = depth0.entries;
  stack1 = stack1 == null || stack1 === false ? stack1 : stack1.completed;
  stack1 = typeof stack1 === functionType ? stack1() : stack1;
  buffer += escapeExpression(stack1) + ")\n    </button>\n  ";
  return buffer;}

function program3(depth0,data) {
  
  var buffer = "", stack1, stack2, foundHelper;
  buffer += "\n    ";
  stack1 = depth0.Ember;
  stack1 = stack1 == null || stack1 === false ? stack1 : stack1.Checkbox;
  stack2 = {};
  stack2['checkedBinding'] = "view.content.completed";
  stack2['class'] = "toggle";
  foundHelper = helpers.view;
  stack1 = foundHelper ? foundHelper.call(depth0, stack1, {hash:stack2}) : helperMissing.call(depth0, "view", stack1, {hash:stack2});
  buffer += escapeExpression(stack1) + "\n    <label>";
  stack1 = depth0.view;
  stack1 = stack1 == null || stack1 === false ? stack1 : stack1.content;
  stack1 = stack1 == null || stack1 === false ? stack1 : stack1.title;
  stack1 = typeof stack1 === functionType ? stack1() : stack1;
  buffer += escapeExpression(stack1) + "</label>\n    <button ";
  stack1 = depth0.removeItem;
  stack2 = {};
  stack2['target'] = "this";
  foundHelper = helpers.action;
  stack1 = foundHelper ? foundHelper.call(depth0, stack1, {hash:stack2}) : helperMissing.call(depth0, "action", stack1, {hash:stack2});
  buffer += escapeExpression(stack1) + " class=\"destroy\" ></button>    ";
  return buffer;}

function program5(depth0,data) {
  
  var buffer = "", stack1, stack2, foundHelper;
  buffer += "\n    ";
  stack1 = depth0.view;
  stack1 = stack1 == null || stack1 === false ? stack1 : stack1.ItemEditorView;
  stack2 = {};
  stack2['contentBinding'] = "view.content";
  foundHelper = helpers.view;
  stack1 = foundHelper ? foundHelper.call(depth0, stack1, {hash:stack2}) : helperMissing.call(depth0, "view", stack1, {hash:stack2});
  buffer += escapeExpression(stack1) + "\n  ";
  return buffer;}

  buffer += "<script id=\"clearBtnTemplate\" type=\"text/x-handlebars\">\n  ";
  stack1 = depth0.view;
  stack1 = helpers['with'].call(depth0, stack1, {hash:{},inverse:self.noop,fn:self.program(1, program1, data)});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</script>\n<script id=\"todosTemplate\" type=\"text/x-handlebars\">    ";
  stack1 = depth0.view;
  stack1 = stack1 == null || stack1 === false ? stack1 : stack1.content;
  stack1 = stack1 == null || stack1 === false ? stack1 : stack1.editing;
  stack1 = helpers.unless.call(depth0, stack1, {hash:{},inverse:self.program(5, program5, data),fn:self.program(3, program3, data)});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</script>\n";
  return buffer;});
})();
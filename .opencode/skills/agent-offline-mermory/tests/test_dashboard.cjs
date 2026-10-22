const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../assets/templates/dashboard-obsidian.md'), 'utf8').split('```dataviewjs')[1].split('```')[0];
const element = () => ({
  classList: {add() {}}, style: {setProperty() {}}, addEventListener() {},
  querySelectorAll: () => [], querySelector: () => element(), closest: () => null,
});
const root = element();
const rows = ['Task','Experience','Principle','Daily'].map(kind => ({
  type: 'agent-' + kind.toLowerCase(), status: 'doing',
  file: {path: 'Memory/' + kind + '/sample.md', name: 'sample', mtime: new Date()},
}));
const context = vm.createContext({
  document: {getElementById: () => null, createElement: element, head: {appendChild() {}}},
  dv: {
    current: () => ({file: {path: 'Memory/Memory.md', name: 'Memory'}}),
    container: root,
    pages: () => ({where: predicate => ({array: () => rows.filter(predicate)})}),
  },
});
vm.runInContext(source, context);
assert.equal((root.innerHTML.match(/class="am-stat-value"/g) || []).length, 4);
assert.ok(root.innerHTML.includes('Memory/Principle/sample.md'));
assert.ok(root.innerHTML.includes('Memory/Experience/sample.md'));
for (const kind of ['task','experience','principle','daily']) {
  const body = vm.runInContext("noteTemplate('" + kind + "', '标题', new Date())", context);
  assert.ok(body.includes('type: agent-' + kind));
  assert.ok(!body.includes('undefined'));
}
assert.equal(vm.runInContext("statusText('doing')", context), '进行中');
assert.equal(vm.runInContext("statusText('todo')", context), '待处理');
console.log('Dashboard rendering, four types and status labels passed (mock Dataview).');

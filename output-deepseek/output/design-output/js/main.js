/**
 * 软件台账管理平台原型交互脚本
 * 提供表格排序、筛选、分页模拟及图表初始化功能
 */

// 模拟数据（实际开发中由后端API提供）
const mockSoftwareData = [
    { id: 1, name: 'Apache Tomcat', type: '开源软件', funcType1: '开发测试', funcType2: '应用服务器', manager: '张三', versions: 5 },
    { id: 2, name: 'MySQL', type: '开源软件', funcType1: '开发测试', funcType2: '数据库', manager: '李四', versions: 3 },
    { id: 3, name: 'Microsoft Office', type: '商业软件', funcType1: '办公', funcType2: '文字处理', manager: '王五', versions: 2 },
    { id: 4, name: 'Jenkins', type: '开源软件', funcType1: '运维管理', funcType2: 'CI/CD', manager: '赵六', versions: 4 },
    { id: 5, name: '自研监控系统', type: '自研软件', funcType1: '运维管理', funcType2: '监控', manager: '钱七', versions: 1 }
];

// 表格排序功能
function sortTable(tableId, columnIndex, isNumeric = false) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const isAscending = table.getAttribute('data-sort-dir') !== 'asc';
    
    rows.sort((a, b) => {
        const aVal = a.children[columnIndex].textContent.trim();
        const bVal = b.children[columnIndex].textContent.trim();
        
        if (isNumeric) {
            const numA = parseFloat(aVal) || 0;
            const numB = parseFloat(bVal) || 0;
            return isAscending ? numA - numB : numB - numA;
        } else {
            return isAscending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
        }
    });
    
    // 移除旧行
    rows.forEach(row => tbody.removeChild(row));
    // 添加排序后的行
    rows.forEach(row => tbody.appendChild(row));
    
    // 更新排序指示器
    table.querySelectorAll('th').forEach(th => th.classList.remove('sorted-asc', 'sorted-desc'));
    const header = table.querySelector(`th:nth-child(${columnIndex + 1})`);
    if (header) {
        header.classList.add(isAscending ? 'sorted-asc' : 'sorted-desc');
    }
    
    table.setAttribute('data-sort-dir', isAscending ? 'asc' : 'desc');
}

// 表格筛选功能（简单前端筛选）
function filterTable(tableId, filterValues) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        let show = true;
        filterValues.forEach((value, index) => {
            if (value) {
                const cellText = row.children[index].textContent.toLowerCase();
                if (!cellText.includes(value.toLowerCase())) {
                    show = false;
                }
            }
        });
        row.style.display = show ? '' : 'none';
    });
}

// 分页模拟
function initPagination(tableId, pageSize = 10) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    const pageCount = Math.ceil(rows.length / pageSize);
    
    // 创建分页控件
    const pagination = document.createElement('div');
    pagination.className = 'pagination';
    
    for (let i = 1; i <= pageCount; i++) {
        const pageItem = document.createElement('a');
        pageItem.href = '#';
        pageItem.className = 'page-link';
        pageItem.textContent = i;
        pageItem.addEventListener('click', (e) => {
            e.preventDefault();
            showPage(tableId, i, pageSize);
            // 更新活跃页样式
            pagination.querySelectorAll('.page-link').forEach(link => link.classList.remove('active'));
            pageItem.classList.add('active');
        });
        pagination.appendChild(pageItem);
    }
    
    table.parentNode.appendChild(pagination);
    showPage(tableId, 1, pageSize);
    pagination.children[0].classList.add('active');
}

function showPage(tableId, pageNum, pageSize) {
    const table = document.getElementById(tableId);
    const rows = table.querySelectorAll('tbody tr');
    const start = (pageNum - 1) * pageSize;
    const end = start + pageSize;
    
    rows.forEach((row, index) => {
        row.style.display = (index >= start && index < end) ? '' : 'none';
    });
}

// 初始化ECharts图表（需确保已引入ECharts库）
function initChart(containerId, option) {
    const chart = echarts.init(document.getElementById(containerId));
    chart.setOption(option);
    window.addEventListener('resize', () => chart.resize());
    return chart;
}

// 示例图表配置
const exampleChartOption = {
    title: { text: '软件类型分布', left: 'center' },
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', left: 'left' },
    series: [
        {
            name: '软件类型',
            type: 'pie',
            radius: '50%',
            data: [
                { value: 335, name: '开源软件' },
                { value: 310, name: '商业软件' },
                { value: 234, name: '自研软件' }
            ],
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('原型页面加载完成');
    
    // 为所有可排序表格的表头添加点击事件
    document.querySelectorAll('table.sortable th').forEach((th, index) => {
        th.style.cursor = 'pointer';
        th.addEventListener('click', () => {
            const isNumeric = th.classList.contains('numeric');
            sortTable(th.closest('table').id, index, isNumeric);
        });
    });
    
    // 初始化分页（如果页面有需要分页的表格）
    document.querySelectorAll('table.paginated').forEach(table => {
        initPagination(table.id, 5); // 每页5条，方便测试
    });
    
    // 初始化图表（如果页面有图表容器）
    if (typeof echarts !== 'undefined') {
        document.querySelectorAll('.chart-container').forEach(container => {
            // 根据容器ID或数据属性定制图表
            const chartType = container.dataset.chartType || 'pie';
            if (chartType === 'pie') {
                initChart(container.id, exampleChartOption);
            }
            // 可扩展其他图表类型
        });
    }
    
    // 筛选表单提交事件
    document.querySelectorAll('.filter-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const filterValues = Array.from(this.elements)
                .filter(el => el.name)
                .map(el => el.value);
            const tableId = this.dataset.tableTarget;
            filterTable(tableId, filterValues);
        });
    });
});

// 导出函数供全局使用
window.prototypeUtils = {
    sortTable,
    filterTable,
    initPagination,
    initChart
};
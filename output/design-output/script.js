// 全局变量
let currentView = 'grid';
let currentRating = 0;

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    initializeViewToggle();
    initializeSearch();
    initializeRating();
});

// 视图切换功能
function initializeViewToggle() {
    const viewBtns = document.querySelectorAll('.view-btn');
    const gridView = document.getElementById('grid-view');
    const listView = document.getElementById('list-view');

    if (viewBtns.length === 0 || !gridView || !listView) return;

    viewBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const view = this.getAttribute('data-view');
            
            // 更新按钮状态
            viewBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // 切换视图
            if (view === 'grid') {
                gridView.style.display = 'grid';
                listView.style.display = 'none';
                currentView = 'grid';
            } else {
                gridView.style.display = 'none';
                listView.style.display = 'block';
                currentView = 'list';
            }
        });
    });
}

// 搜索功能
function initializeSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');
    
    if (!searchInput || !searchBtn) return;

    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
}

function performSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchValue = searchInput.value.trim();
    
    if (searchValue) {
        console.log('搜索:', searchValue);
        // 这里可以实现实际的搜索逻辑
        alert('搜索功能待实现，搜索关键词：' + searchValue);
    }
}

// 评分功能
function initializeRating() {
    const starBtns = document.querySelectorAll('.star-btn');
    
    starBtns.forEach((btn, index) => {
        btn.addEventListener('click', function() {
            setRating(index + 1);
        });
    });
}

function setRating(rating) {
    currentRating = rating;
    const starBtns = document.querySelectorAll('.star-btn');
    
    starBtns.forEach((btn, index) => {
        if (index < rating) {
            btn.classList.add('active');
            btn.textContent = '★';
        } else {
            btn.classList.remove('active');
            btn.textContent = '☆';
        }
    });
}

// 评价弹窗功能
function showReviewForm() {
    const modal = document.getElementById('review-modal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function hideReviewForm() {
    const modal = document.getElementById('review-modal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        resetReviewForm();
    }
}

function resetReviewForm() {
    setRating(0);
    const textarea = document.querySelector('#review-modal textarea');
    if (textarea) {
        textarea.value = '';
    }
}

function submitReview() {
    if (currentRating === 0) {
        alert('请选择评分');
        return;
    }
    
    const textarea = document.querySelector('#review-modal textarea');
    const reviewContent = textarea ? textarea.value.trim() : '';
    
    if (reviewContent === '') {
        alert('请填写评价内容');
        return;
    }
    
    console.log('提交评价:', {
        rating: currentRating,
        content: reviewContent
    });
    
    alert('评价提交成功！');
    hideReviewForm();
}

// 软件详情页面的动态内容加载
function loadSoftwareDetail() {
    // 从URL参数获取软件类型和ID
    const urlParams = new URLSearchParams(window.location.search);
    const type = urlParams.get('type') || 'product';
    const id = urlParams.get('id') || '1';
    
    // 根据类型和ID加载不同的软件信息
    const softwareData = getSoftwareData(type, id);
    updateDetailPage(softwareData, type);
}

function getSoftwareData(type, id) {
    // 模拟软件数据
    const data = {
        'product-1': {
            name: '飞书',
            type: '商业软件',
            category: '产品类',
            function: '办公软件',
            license: '商业许可',
            version: 'v6.5.0',
            description: '飞书是一款企业协作办公平台，支持即时通讯、文档协作、视频会议、日程管理等功能，为企业提供一站式办公解决方案。',
            downloads: '2,456',
            rating: '4.6'
        },
        'component-2': {
            name: 'org.springframework.boot:spring-boot-starter',
            type: '开源软件',
            category: '组件类',
            function: '开发组件',
            license: 'Apache 2.0',
            version: '2.7.14',
            description: 'Spring Boot应用启动器，提供快速构建生产级Spring应用程序的功能，简化了Spring应用的初始搭建和开发过程。',
            downloads: '3,789',
            rating: '4.8'
        }
    };
    
    const key = `${type}-${id}`;
    return data[key] || data['product-1'];
}

function updateDetailPage(data, type) {
    // 更新基础信息
    const nameEl = document.getElementById('software-name');
    const detailNameEl = document.getElementById('detail-name');
    const typeEl = document.getElementById('detail-type');
    const categoryEl = document.getElementById('detail-category');
    const functionEl = document.getElementById('detail-function');
    const licenseEl = document.getElementById('detail-license');
    const versionEl = document.getElementById('detail-version');
    const descriptionEl = document.getElementById('detail-description');
    
    if (nameEl) nameEl.textContent = data.name;
    if (detailNameEl) detailNameEl.textContent = data.name;
    if (typeEl) typeEl.textContent = data.type;
    if (categoryEl) categoryEl.textContent = data.category;
    if (functionEl) functionEl.textContent = data.function;
    if (licenseEl) licenseEl.textContent = data.license;
    if (versionEl) versionEl.textContent = data.version;
    if (descriptionEl) descriptionEl.textContent = data.description;
    
    // 更新操作按钮
    const downloadBtn = document.getElementById('download-btn');
    const externalBtn = document.getElementById('external-btn');
    
    if (type === 'product') {
        if (downloadBtn) downloadBtn.style.display = 'inline-block';
        if (externalBtn) externalBtn.style.display = 'none';
    } else {
        if (downloadBtn) downloadBtn.style.display = 'none';
        if (externalBtn) externalBtn.style.display = 'inline-block';
    }
    
    // 更新统计信息
    updateStats(data.downloads, data.rating);
    
    // 更新徽章
    updateBadges(data.type, data.category);
}

function updateStats(downloads, rating) {
    const statItems = document.querySelectorAll('.stat-number');
    if (statItems.length >= 1) statItems[0].textContent = downloads;
    if (statItems.length >= 3) statItems[2].textContent = rating;
}

function updateBadges(type, category) {
    const badges = document.querySelectorAll('.software-badges .badge');
    
    // 更新类型徽章
    if (badges[0]) {
        badges[0].textContent = type;
        badges[0].className = 'badge type-badge';
        if (type === '商业软件') {
            badges[0].classList.add('commercial');
        } else if (type === '开源软件') {
            badges[0].classList.add('opensource');
        } else if (type === '自主软件') {
            badges[0].classList.add('self');
        }
    }
    
    // 更新分类徽章
    if (badges[1]) {
        badges[1].textContent = category;
        badges[1].className = 'badge category-badge';
        if (category === '产品类') {
            badges[1].classList.add('product');
        } else if (category === '组件类') {
            badges[1].classList.add('component');
        }
    }
}

// 筛选功能
function initializeFilters() {
    const filterSelects = document.querySelectorAll('.filter-select');
    const filterBtn = document.querySelector('.filter-btn');
    
    if (filterBtn) {
        filterBtn.addEventListener('click', resetFilters);
    }
    
    filterSelects.forEach(select => {
        select.addEventListener('change', applyFilters);
    });
}

function applyFilters() {
    const typeFilter = document.querySelector('.filter-select:nth-child(1)').value;
    const categoryFilter = document.querySelector('.filter-select:nth-child(2)').value;
    const functionFilter = document.querySelector('.filter-select:nth-child(3)').value;
    const licenseFilter = document.querySelector('.filter-select:nth-child(4)').value;
    
    console.log('应用筛选:', {
        type: typeFilter,
        category: categoryFilter,
        function: functionFilter,
        license: licenseFilter
    });
    
    // 这里可以实现实际的筛选逻辑
    filterSoftwareItems(typeFilter, categoryFilter, functionFilter, licenseFilter);
}

function filterSoftwareItems(typeFilter, categoryFilter, functionFilter, licenseFilter) {
    const cards = document.querySelectorAll('.software-card');
    
    cards.forEach(card => {
        let show = true;
        
        // 获取卡片的属性
        const type = card.getAttribute('data-type');
        const category = card.getAttribute('data-category');
        const func = card.getAttribute('data-function');
        const license = card.getAttribute('data-license');
        
        // 应用筛选条件
        if (typeFilter && type !== typeFilter) show = false;
        if (categoryFilter && category !== categoryFilter) show = false;
        if (functionFilter && func !== functionFilter) show = false;
        if (licenseFilter && license !== licenseFilter) show = false;
        
        // 显示或隐藏卡片
        card.style.display = show ? 'block' : 'none';
    });
}

function resetFilters() {
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(select => {
        select.value = '';
    });
    
    // 显示所有卡片
    const cards = document.querySelectorAll('.software-card');
    cards.forEach(card => {
        card.style.display = 'block';
    });
}

// 分页功能
function initializePagination() {
    const pageBtns = document.querySelectorAll('.page-btn');
    
    pageBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.disabled) return;
            
            const pageNum = this.textContent;
            if (!isNaN(pageNum)) {
                goToPage(parseInt(pageNum));
            } else if (this.textContent === '上一页') {
                previousPage();
            } else if (this.textContent === '下一页') {
                nextPage();
            }
        });
    });
}

function goToPage(pageNum) {
    console.log('跳转到第', pageNum, '页');
    // 这里可以实现实际的分页逻辑
    updatePaginationState(pageNum);
}

function previousPage() {
    console.log('上一页');
    // 实现上一页逻辑
}

function nextPage() {
    console.log('下一页');
    // 实现下一页逻辑
}

function updatePaginationState(currentPage) {
    const pageBtns = document.querySelectorAll('.page-btn');
    
    pageBtns.forEach(btn => {
        if (btn.textContent == currentPage) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// 排序功能
function initializeSort() {
    const sortSelect = document.querySelector('.sort-select');
    
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const sortBy = this.value;
            sortSoftwareList(sortBy);
        });
    }
}

function sortSoftwareList(sortBy) {
    console.log('按', sortBy, '排序');
    // 这里可以实现实际的排序逻辑
}

// 导出功能
function exportSoftwareList() {
    console.log('导出软件列表');
    alert('导出功能待实现');
}

// 收藏功能
function toggleFavorite(button) {
    const isFavorited = button.classList.contains('favorited');
    
    if (isFavorited) {
        button.classList.remove('favorited');
        button.textContent = '收藏';
        console.log('取消收藏');
    } else {
        button.classList.add('favorited');
        button.textContent = '已收藏';
        console.log('添加收藏');
    }
}

// 下载功能
function downloadSoftware(softwareId) {
    console.log('下载软件:', softwareId);
    alert('下载功能待实现');
}

// 跳转下载功能（组件类软件）
function redirectToDownload(url) {
    console.log('跳转到下载页面:', url);
    // 白名单验证
    if (isWhitelistUrl(url)) {
        window.open(url, '_blank');
    } else {
        alert('该下载链接不在白名单中，请联系管理员添加');
    }
}

function isWhitelistUrl(url) {
    // 模拟白名单检查
    const whitelist = [
        'https://search.maven.org/',
        'https://repo.maven.apache.org/',
        'https://central.sonatype.com/'
    ];
    
    return whitelist.some(whitelistUrl => url.startsWith(whitelistUrl));
}

// 权限检查
function checkPermission(action) {
    // 模拟权限检查
    const userRole = 'admin'; // 可以从全局状态获取
    
    const permissions = {
        admin: ['view', 'download', 'edit', 'delete', 'manage'],
        manager: ['view', 'download', 'edit'],
        user: ['view', 'download']
    };
    
    return permissions[userRole] && permissions[userRole].includes(action);
}

// 退出登录
function logout() {
    if (confirm('确定要退出登录吗？')) {
        console.log('退出登录');
        // 清除用户状态
        // 跳转到登录页面
        alert('退出登录成功');
    }
}

// 添加退出登录事件监听
document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
    
    // 如果是详情页面，加载详情数据
    if (window.location.pathname.includes('software-detail.html')) {
        loadSoftwareDetail();
    }
    
    // 如果是统计分析页面，初始化图表
    if (window.location.pathname.includes('statistics.html')) {
        initializeCharts();
    }
    
    // 如果是用户管理页面，初始化用户管理功能
    if (window.location.pathname.includes('user-management.html')) {
        initializeUserManagement();
    }
    
    // 初始化其他功能
    initializeFilters();
    initializePagination();
    initializeSort();
    
    // 添加收藏按钮事件
    const favoriteBtns = document.querySelectorAll('.btn[onclick*="favorite"]');
    favoriteBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            toggleFavorite(this);
        });
    });
});

// 用户管理初始化
function initializeUserManagement() {
    // 全选功能
    const selectAll = document.getElementById('selectAll');
    if (selectAll) {
        selectAll.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('.user-table input[type="checkbox"]:not(#selectAll)');
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
    }
    
    // 搜索功能
    const userSearchBtn = document.querySelector('.user-filters .search-btn');
    const userSearchInput = document.querySelector('.user-filters .search-input');
    
    if (userSearchBtn) {
        userSearchBtn.addEventListener('click', performUserSearch);
    }
    
    if (userSearchInput) {
        userSearchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performUserSearch();
            }
        });
    }
    
    // 筛选功能
    const userFilterSelects = document.querySelectorAll('.user-filters .filter-select');
    userFilterSelects.forEach(select => {
        select.addEventListener('change', applyUserFilters);
    });
    
    // 重置按钮
    const userFilterBtn = document.querySelector('.user-filters .filter-btn');
    if (userFilterBtn) {
        userFilterBtn.addEventListener('click', resetUserFilters);
    }
    
    // 导出按钮
    const exportBtn = document.querySelector('.action-buttons .btn-secondary');
    if (exportBtn && exportBtn.textContent.includes('导出')) {
        exportBtn.addEventListener('click', exportUserList);
    }
}

function performUserSearch() {
    const searchInput = document.querySelector('.user-filters .search-input');
    const searchValue = searchInput.value.trim();
    
    if (searchValue) {
        console.log('搜索用户:', searchValue);
        // 实现用户搜索逻辑
    }
}

function applyUserFilters() {
    const roleFilter = document.querySelector('.user-filters .filter-select:nth-child(1)').value;
    const departmentFilter = document.querySelector('.user-filters .filter-select:nth-child(2)').value;
    const statusFilter = document.querySelector('.user-filters .filter-select:nth-child(3)').value;
    
    console.log('用户筛选:', { roleFilter, departmentFilter, statusFilter });
    // 实现用户筛选逻辑
}

function resetUserFilters() {
    const filterSelects = document.querySelectorAll('.user-filters .filter-select');
    filterSelects.forEach(select => {
        select.value = '';
    });
    
    const searchInput = document.querySelector('.user-filters .search-input');
    if (searchInput) {
        searchInput.value = '';
    }
}

// 工具函数
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN');
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// 模拟数据加载
function loadMockData() {
    console.log('加载模拟数据...');
    // 这里可以添加模拟数据加载逻辑
}

// 错误处理
window.addEventListener('error', function(e) {
    console.error('页面错误:', e.error);
});

// 页面性能监控
window.addEventListener('load', function() {
    const loadTime = performance.now();
    console.log('页面加载时间:', loadTime, 'ms');
    
    // 为导出按钮添加事件
    const exportButtons = document.querySelectorAll('.btn');
    exportButtons.forEach(btn => {
        if (btn.textContent.includes('导出报告')) {
            btn.addEventListener('click', exportStatistics);
        }
    });
});

// 用户管理功能
function showAddUserModal() {
    const modal = document.getElementById('addUserModal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function hideAddUserModal() {
    const modal = document.getElementById('addUserModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        clearAddUserForm();
    }
}

function clearAddUserForm() {
    const inputs = document.querySelectorAll('#addUserModal input[type="text"], #addUserModal input[type="email"], #addUserModal input[type="password"]');
    const selects = document.querySelectorAll('#addUserModal select');
    
    inputs.forEach(input => input.value = '');
    selects.forEach(select => select.selectedIndex = 0);
}

function addUser() {
    const username = document.querySelector('#addUserModal input[type="text"]').value.trim();
    const email = document.querySelector('#addUserModal input[type="email"]').value.trim();
    const department = document.querySelector('#addUserModal select').value;
    const role = document.querySelectorAll('#addUserModal select')[1].value;
    
    if (!username || !email || !department || !role) {
        alert('请填写所有必填字段');
        return;
    }
    
    console.log('添加用户:', { username, email, department, role });
    alert('用户添加成功！');
    hideAddUserModal();
}

function editUser(userId) {
    // 模拟获取用户数据
    const userData = getUserData(userId);
    
    // 填充表单
    document.getElementById('editUsername').value = userData.username;
    document.getElementById('editEmail').value = userData.email;
    document.getElementById('editDepartment').value = userData.department;
    document.getElementById('editRole').value = userData.role;
    document.getElementById('editStatus').value = userData.status;
    
    // 显示模态框
    const modal = document.getElementById('editUserModal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        modal.dataset.userId = userId;
    }
}

function hideEditUserModal() {
    const modal = document.getElementById('editUserModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        delete modal.dataset.userId;
    }
}

function updateUser() {
    const modal = document.getElementById('editUserModal');
    const userId = modal.dataset.userId;
    
    const userData = {
        username: document.getElementById('editUsername').value,
        email: document.getElementById('editEmail').value,
        department: document.getElementById('editDepartment').value,
        role: document.getElementById('editRole').value,
        status: document.getElementById('editStatus').value
    };
    
    console.log('更新用户:', userId, userData);
    alert('用户信息更新成功！');
    hideEditUserModal();
}

function getUserData(userId) {
    // 模拟用户数据
    const users = {
        '1': { username: 'admin', email: 'admin@company.com', department: 'tech', role: 'super_admin', status: 'active' },
        '2': { username: '张三', email: 'zhangsan@company.com', department: 'tech', role: 'dept_admin', status: 'active' },
        '3': { username: '李四', email: 'lisi@company.com', department: 'product', role: 'dept_admin', status: 'active' },
        '4': { username: '王五', email: 'wangwu@company.com', department: 'tech', role: 'user', status: 'active' },
        '5': { username: '赵六', email: 'zhaoliu@company.com', department: 'marketing', role: 'user', status: 'inactive' }
    };
    
    return users[userId] || users['1'];
}

function showBatchImportModal() {
    alert('批量导入功能待实现');
}

// 统计图表交互
function initializeCharts() {
    // 图表按钮切换
    const chartBtns = document.querySelectorAll('.chart-btn');
    chartBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const parent = this.closest('.chart-controls');
            parent.querySelectorAll('.chart-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // 筛选标签切换
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const parent = this.closest('.filter-tabs');
            parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // 时间范围选择
    const timeRange = document.querySelector('.time-range');
    if (timeRange) {
        timeRange.addEventListener('change', function() {
            console.log('切换时间范围:', this.value);
            // 这里可以更新图表数据
        });
    }
    
    // 警报按钮切换
    const alertBtns = document.querySelectorAll('.alert-btn');
    alertBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const parent = this.closest('.alert-controls');
            parent.querySelectorAll('.alert-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// 导出功能
function exportUserList() {
    console.log('导出用户列表');
    alert('用户列表导出功能待实现');
}

function exportStatistics() {
    console.log('导出统计报告');
    alert('统计报告导出功能待实现');
}

// 导出全局函数（供HTML调用）
window.showReviewForm = showReviewForm;
window.hideReviewForm = hideReviewForm;
window.submitReview = submitReview;
window.setRating = setRating;
window.redirectToDownload = redirectToDownload;
window.showAddUserModal = showAddUserModal;
window.hideAddUserModal = hideAddUserModal;
window.addUser = addUser;
window.editUser = editUser;
window.hideEditUserModal = hideEditUserModal;
window.updateUser = updateUser;
window.showBatchImportModal = showBatchImportModal;
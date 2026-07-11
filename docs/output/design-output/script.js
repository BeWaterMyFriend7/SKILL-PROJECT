// 软件台账管理平台 - 交互脚本

document.addEventListener('DOMContentLoaded', function() {
    // 权限配置
    const rolePermissions = {
        'super_admin': {
            name: '超管',
            canViewAll: true,
            canViewLevel2: true,
            canViewSync: true,
            usagePages: ['terminal', 'app', 'server']
        },
        'team_leader': {
            name: '团队负责人',
            canViewAll: false,
            canViewLevel2: true,
            canViewSync: false,
            usagePages: ['terminal', 'app', 'server']
        },
        'owner': {
            name: '负责人本人',
            canViewAll: false,
            canViewLevel2: false,
            canViewSync: false,
            usagePages: ['terminal', 'app', 'server']
        },
        'normal': {
            name: '普通用户',
            canViewAll: false,
            canViewLevel2: false,
            canViewSync: false,
            usagePages: []
        }
    };

    let currentRole = 'super_admin';

    // 角色切换
    const roleSwitcher = document.getElementById('roleSwitcher');
    const currentRoleEl = document.getElementById('currentRole');
    
    roleSwitcher.addEventListener('change', function() {
        currentRole = this.value;
        currentRoleEl.textContent = rolePermissions[currentRole].name;
        updateAllPermissions();
    });

    // 更新所有权限相关显示
    function updateAllPermissions() {
        updateUsagePagePermissions();
        updateStatisticsPermissions();
    }

    // 更新使用关系页面权限
    function updateUsagePagePermissions() {
        const pages = ['terminal', 'app', 'server'];
        const perm = rolePermissions[currentRole];
        
        pages.forEach(page => {
            const noticeEl = document.getElementById('perm-notice-' + page);
            const roleTextEl = document.getElementById('role-text-' + page);
            
            if (noticeEl && roleTextEl) {
                roleTextEl.textContent = perm.name;
                
                if (perm.canViewAll) {
                    noticeEl.className = 'permission-notice';
                    noticeEl.querySelector('.notice-text').innerHTML = 
                        `当前角色：<strong>${perm.name}</strong> - 可查看全部数据`;
                } else if (perm.usagePages.includes(page)) {
                    noticeEl.className = 'permission-notice warning';
                    noticeEl.querySelector('.notice-text').innerHTML = 
                        `当前角色：<strong>${perm.name}</strong> - 只能查看本团队/本人相关数据`;
                } else {
                    noticeEl.className = 'permission-notice danger';
                    noticeEl.querySelector('.notice-text').innerHTML = 
                        `当前角色：<strong>${perm.name}</strong> - 无权限查看此数据`;
                }
            }
        });
    }

    // 更新统计大屏权限
    function updateStatisticsPermissions() {
        const perm = rolePermissions[currentRole];
        const level1El = document.getElementById('stats-level1');
        const level2El = document.getElementById('stats-level2');
        const noticeEl = document.getElementById('perm-notice-stats');
        const roleTextEl = document.getElementById('role-text-stats');
        
        if (roleTextEl) {
            roleTextEl.textContent = perm.name;
        }
        
        if (noticeEl) {
            if (perm.canViewLevel2) {
                noticeEl.className = 'permission-notice';
                noticeEl.querySelector('.notice-text').innerHTML = 
                    `当前角色：<strong>${perm.name}</strong> - 可查看全部数据（第一层+第二层+同步状态）`;
            } else {
                noticeEl.className = 'permission-notice warning';
                noticeEl.querySelector('.notice-text').innerHTML = 
                    `当前角色：<strong>${perm.name}</strong> - 只能查看第一层统计数据`;
            }
        }
        
        // 第一层始终显示
        if (level1El) {
            level1El.classList.remove('hidden');
        }
        
        // 第二层根据权限显示
        if (level2El) {
            if (perm.canViewLevel2) {
                level2El.classList.remove('hidden');
            } else {
                level2El.classList.add('hidden');
            }
        }
    }

    // 导航切换
    const navItems = document.querySelectorAll('.nav-item');
    const pages = document.querySelectorAll('.page');
    const quickLinks = document.querySelectorAll('.link-card[data-target]');

    function showPage(pageId) {
        // 隐藏所有页面
        pages.forEach(page => page.classList.remove('active'));
        // 显示目标页面
        const targetPage = document.getElementById('page-' + pageId);
        if (targetPage) {
            targetPage.classList.add('active');
        }
        // 更新导航状态
        navItems.forEach(item => {
            if (item.dataset.page === pageId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
        
        // 更新当前页面权限显示
        if (pageId === 'usage-terminal' || pageId === 'usage-app' || pageId === 'usage-server') {
            updateUsagePagePermissions();
        } else if (pageId === 'statistics') {
            updateStatisticsPermissions();
        }
        
        // 滚动到顶部
        window.scrollTo(0, 0);
    }

    // 顶部导航点击
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.dataset.page;
            if (page) {
                showPage(page);
            }
        });
    });

    // 首页快速入口点击
    quickLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.dataset.target;
            if (target) {
                showPage(target);
            }
        });
    });

    // ===== 问题1修复：软件列表页跳转到详情页 =====
    // 点击表格行跳转
    const tableRows = document.querySelectorAll('.clickable-row');
    tableRows.forEach(row => {
        row.addEventListener('click', function(e) {
            // 如果点击的是按钮，不触发跳转
            if (e.target.tagName === 'BUTTON') return;
            
            const softwareId = this.dataset.id;
            if (softwareId) {
                // 跳转到详情页（新窗口打开）
                window.open('software-detail.html?id=' + softwareId, '_blank');
            }
        });
    });

    // 点击查看按钮跳转
    const viewButtons = document.querySelectorAll('.btn-view-detail');
    viewButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const softwareId = this.dataset.id;
            if (softwareId) {
                window.open('software-detail.html?id=' + softwareId, '_blank');
            }
        });
    });

    // Tab 切换
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tab = this.dataset.tab;
            const parent = this.closest('.page');
            
            // 更新tab状态
            parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            console.log('切换到:', tab);
        });
    });

    // 搜索功能
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                console.log('搜索:', this.value);
            }
        });
    });

    // 筛选按钮
    const filterBtns = document.querySelectorAll('.filter-bar .btn-secondary');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            console.log('筛选');
        });
    });

    // 分页
    const pageBtns = document.querySelectorAll('.btn-page');
    pageBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.disabled || this.classList.contains('active')) return;
            
            const parent = this.closest('.pagination');
            const pageInfo = parent.querySelector('.page-info');
            
            // 更新按钮状态
            parent.querySelectorAll('.btn-page').forEach(b => {
                if (!b.disabled) b.classList.remove('active');
            });
            
            if (!isNaN(this.textContent)) {
                this.classList.add('active');
            }
            
            console.log('切换页码');
        });
    });

    // ========== 主Tab切换：统计大屏 | 同步情况 ==========
    const mainTabBtns = document.querySelectorAll('.main-tab-btn');
    const mainTabPanels = document.querySelectorAll('.main-tab-panel');
    
    mainTabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.dataset.mainTab;
            
            // 更新按钮状态
            mainTabBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // 更新面板显示
            mainTabPanels.forEach(panel => {
                panel.classList.remove('active');
                if (panel.id === 'main-tab-' + tabId) {
                    panel.classList.add('active');
                }
            });
            
            // 如果切换到同步Tab，检查权限
            if (tabId === 'sync') {
                checkSyncPermission();
            }
        });
    });
    
    // 检查同步Tab权限
    function checkSyncPermission() {
        const perm = rolePermissions[currentRole];
        const syncPanel = document.getElementById('main-tab-sync');
        
        if (!perm.canViewSync) {
            // 无权限，显示提示
            syncPanel.innerHTML = `
                <div class="permission-notice danger" style="margin-top: 20px;">
                    <span class="notice-icon">🔒</span>
                    <span class="notice-text">您无权限查看同步情况，仅<strong>超管</strong>可查看</span>
                </div>
            `;
        }
    }

    // ========== 同步情况子Tab切换 ==========
    const syncTabBtns = document.querySelectorAll('.sync-tab-btn');
    const syncTabPanels = document.querySelectorAll('.sync-tab-panel');
    
    syncTabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.dataset.syncTab;
            
            // 更新按钮状态
            syncTabBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // 更新面板显示
            syncTabPanels.forEach(panel => {
                panel.classList.remove('active');
                if (panel.id === 'sync-' + tabId) {
                    panel.classList.add('active');
                }
            });
        });
    });

    // ========== 细分统计收起/展开 ==========
    const toggleDetailBtn = document.getElementById('toggleDetailStats');
    const detailStatsContent = document.getElementById('detail-stats-content');
    let detailStatsExpanded = true;
    
    if (toggleDetailBtn) {
        toggleDetailBtn.addEventListener('click', function() {
            detailStatsExpanded = !detailStatsExpanded;
            if (detailStatsExpanded) {
                detailStatsContent.classList.remove('hidden');
                this.textContent = '收起详情 ▲';
            } else {
                detailStatsContent.classList.add('hidden');
                this.textContent = '展开详情 ▼';
            }
        });
    }

    // 初始化权限显示
    updateAllPermissions();

    console.log('软件台账管理平台已加载');
});

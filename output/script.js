let softwareData = [];
let filteredData = [];

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    loadSoftwareData();
});

// 加载软件数据
async function loadSoftwareData() {
    try {
        // 尝试从本地存储获取数据
        const cachedData = localStorage.getItem('softwareData');
        if (cachedData) {
            softwareData = JSON.parse(cachedData);
        } else {
            // 如果本地存储没有，尝试从文件加载
            try {
                const response = await fetch('software-data.txt');
                const data = await response.text();
                softwareData = JSON.parse(data);
                localStorage.setItem('softwareData', data);
            } catch (fetchError) {
                console.warn('无法加载文件数据，使用内置数据:', fetchError);
                // 使用内置的示例数据
                softwareData = getSampleData();
                localStorage.setItem('softwareData', JSON.stringify(softwareData));
            }
        }
        
        filteredData = [...softwareData];
        renderSoftwareList(filteredData);
        updateResultsCount(filteredData.length);
    } catch (error) {
        console.error('加载软件数据失败:', error);
        // 最后的备用方案
        softwareData = getSampleData();
        filteredData = [...softwareData];
        renderSoftwareList(filteredData);
        updateResultsCount(filteredData.length);
    }
}

// 获取示例数据
function getSampleData() {
    return [
        {
            id: 1,
            name: "Visual Studio Code",
            type: "开源",
            license: "MIT",
            description: "轻量级但功能强大的源代码编辑器，支持多种编程语言",
            image: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Visual_Studio_Code_1.35.1.svg/1200px-Visual_Studio_Code_1.35.1.svg.png",
            scope: "全公司",
            tags: ["编辑器", "开发工具", "跨平台"],
            category: "开发工具",
            versions: [
                {
                    version: "1.85.0",
                    downloadUrl: "#",
                    description: "最新稳定版本"
                },
                {
                    version: "1.82.0",
                    downloadUrl: "#",
                    description: "LTS长期支持版本"
                }
            ],
            manual: "#",
            rating: 4.8,
            documents: ["安装指南.pdf", "使用手册.pdf"]
        },
        {
            id: 2,
            name: "Office 365",
            type: "商业",
            license: "微软商业许可",
            description: "Microsoft Office办公套件，包含Word、Excel、PowerPoint等应用",
            image: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Microsoft_Office_365_logo.svg/1200px-Microsoft_Office_365_logo.svg.png",
            scope: "全公司",
            tags: ["办公", "文档处理", "表格", "演示"],
            category: "办公软件",
            versions: [
                {
                    version: "2023",
                    downloadUrl: "#",
                    description: "最新版本，包含AI功能"
                },
                {
                    version: "2021",
                    downloadUrl: "#",
                    description: "稳定版本"
                }
            ],
            manual: "#",
            rating: 4.5,
            documents: ["部署指南.pdf", "许可证说明.pdf"]
        },
        {
            id: 3,
            name: "企业微信",
            type: "商业",
            license: "腾讯商业许可",
            description: "企业级即时通讯和协作平台，集成办公、沟通、管理功能",
            image: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/WeChat_Work_logo.svg/1200px-WeChat_Work_logo.svg.png",
            scope: "全公司",
            tags: ["通讯", "协作", "移动办公"],
            category: "通讯协作",
            versions: [
                {
                    version: "4.0.0",
                    downloadUrl: "#",
                    description: "最新版本"
                }
            ],
            manual: "#",
            rating: 4.3,
            documents: ["管理员手册.pdf", "用户指南.pdf"]
        },
        {
            id: 4,
            name: "Git",
            type: "开源",
            license: "GPLv2",
            description: "分布式版本控制系统，用于代码管理和协作开发",
            image: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Git-logo.svg/1200px-Git-logo.svg.png",
            scope: "研发部门",
            tags: ["版本控制", "开发工具", "开源"],
            category: "开发工具",
            versions: [
                {
                    version: "2.42.0",
                    downloadUrl: "#",
                    description: "最新稳定版"
                },
                {
                    version: "2.40.0",
                    downloadUrl: "#",
                    description: "LTS版本"
                }
            ],
            manual: "#",
            rating: 4.7,
            documents: ["Git教程.pdf", "命令参考.pdf"]
        },
        {
            id: 5,
            name: "内部CRM系统",
            type: "自研",
            license: "内部使用",
            description: "自主研发的客户关系管理系统，集成销售、客服、市场营销功能",
            image: "https://via.placeholder.com/300x200/4A90E2/FFFFFF?text=CRM",
            scope: "销售、客服、市场部门",
            tags: ["CRM", "客户管理", "自研"],
            category: "业务系统",
            versions: [
                {
                    version: "3.2.1",
                    downloadUrl: "#",
                    description: "当前生产版本"
                },
                {
                    version: "3.1.0",
                    downloadUrl: "#",
                    description: "稳定版本"
                }
            ],
            manual: "#",
            rating: 4.2,
            documents: ["用户手册.pdf", "管理员指南.pdf", "API文档.pdf"]
        }
    ];
}

// 渲染软件列表
function renderSoftwareList(data) {
    const grid = document.getElementById('softwareGrid');
    if (!grid) return;

    if (data.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: #666;">没有找到符合条件的软件</div>';
        return;
    }

    grid.innerHTML = data.map(software => `
        <div class="software-card" onclick="goToDetail(${software.id})">
            <div class="software-header">
                <img src="${software.image}" alt="${software.name}" class="software-image" onerror="this.style.display='none'">
                <div class="software-info">
                    <h3>${software.name}</h3>
                    <span class="software-type ${getTypeClass(software.type)}">${software.type}</span>
                </div>
            </div>
            <div class="software-description">
                ${software.description}
            </div>
            <div class="software-meta">
                <div class="meta-item">
                    <strong>开源协议:</strong> ${software.license || '不适用'}
                </div>
                <div class="meta-item">
                    <strong>使用范围:</strong> ${software.scope}
                </div>
                <div class="meta-item">
                    <strong>功能分类:</strong> ${software.category}
                </div>
            </div>
            <div class="software-tags">
                ${software.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
        </div>
    `).join('');
}

// 获取类型样式类
function getTypeClass(type) {
    switch(type) {
        case '开源': return 'type-open-source';
        case '商业': return 'type-commercial';
        case '自研': return 'type-internal';
        default: return '';
    }
}

// 搜索软件
function searchSoftware() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
    
    if (searchTerm === '') {
        filterSoftware();
        return;
    }

    filteredData = softwareData.filter(software => {
        return software.name.toLowerCase().includes(searchTerm) ||
               software.description.toLowerCase().includes(searchTerm) ||
               software.tags.some(tag => tag.toLowerCase().includes(searchTerm)) ||
               software.category.toLowerCase().includes(searchTerm);
    });

    // 如果有其他筛选条件，也应用
    applyAdditionalFilters();
    
    renderSoftwareList(filteredData);
    updateResultsCount(filteredData.length);
}

// 筛选软件
function filterSoftware() {
    const typeFilter = document.getElementById('typeFilter').value;
    const categoryFilter = document.getElementById('categoryFilter').value;
    const scopeFilter = document.getElementById('scopeFilter').value;

    filteredData = softwareData.filter(software => {
        let match = true;
        
        if (typeFilter && software.type !== typeFilter) {
            match = false;
        }
        
        if (categoryFilter && software.category !== categoryFilter) {
            match = false;
        }
        
        if (scopeFilter && software.scope !== scopeFilter) {
            match = false;
        }
        
        return match;
    });

    // 如果有搜索关键词，也应用搜索筛选
    const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
    if (searchTerm !== '') {
        filteredData = filteredData.filter(software => {
            return software.name.toLowerCase().includes(searchTerm) ||
                   software.description.toLowerCase().includes(searchTerm) ||
                   software.tags.some(tag => tag.toLowerCase().includes(searchTerm)) ||
                   software.category.toLowerCase().includes(searchTerm);
        });
    }
    
    renderSoftwareList(filteredData);
    updateResultsCount(filteredData.length);
}

// 应用额外筛选条件
function applyAdditionalFilters() {
    const typeFilter = document.getElementById('typeFilter').value;
    const categoryFilter = document.getElementById('categoryFilter').value;
    const scopeFilter = document.getElementById('scopeFilter').value;

    if (typeFilter || categoryFilter || scopeFilter) {
        filteredData = filteredData.filter(software => {
            let match = true;
            
            if (typeFilter && software.type !== typeFilter) {
                match = false;
            }
            
            if (categoryFilter && software.category !== categoryFilter) {
                match = false;
            }
            
            if (scopeFilter && software.scope !== scopeFilter) {
                match = false;
            }
            
            return match;
        });
    }
}

// 重置筛选条件
function resetFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('typeFilter').value = '';
    document.getElementById('categoryFilter').value = '';
    document.getElementById('scopeFilter').value = '';
    
    filteredData = [...softwareData];
    renderSoftwareList(filteredData);
    updateResultsCount(filteredData.length);
}

// 更新结果计数
function updateResultsCount(count) {
    const countElement = document.getElementById('resultsCount');
    if (countElement) {
        countElement.textContent = `共找到 ${count} 个软件`;
    }
}

// 跳转到详情页面
function goToDetail(softwareId) {
    // 通过URL参数传递软件ID
    window.location.href = `detail.html?id=${softwareId}`;
}

// 监听Enter键进行搜索
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                searchSoftware();
            }
        });
    }
});
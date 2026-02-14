let currentSoftware = null;

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const softwareId = parseInt(urlParams.get('id'));
    
    if (softwareId) {
        loadSoftwareDetail(softwareId);
    } else {
        showErrorMessage('未找到软件ID');
    }
});

// 加载软件详情
async function loadSoftwareDetail(softwareId) {
    try {
        let softwareData;
        
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
        
        currentSoftware = softwareData.find(software => software.id === softwareId);
        
        if (currentSoftware) {
            renderSoftwareDetail(currentSoftware);
            renderVersions(currentSoftware.versions);
            renderDocuments(currentSoftware.documents);
            renderRating(currentSoftware.rating);
        } else {
            showErrorMessage('未找到指定的软件');
        }
    } catch (error) {
        console.error('加载软件详情失败:', error);
        // 最后的备用方案
        try {
            const softwareData = getSampleData();
            currentSoftware = softwareData.find(software => software.id === softwareId);
            if (currentSoftware) {
                renderSoftwareDetail(currentSoftware);
                renderVersions(currentSoftware.versions);
                renderDocuments(currentSoftware.documents);
                renderRating(currentSoftware.rating);
            } else {
                showErrorMessage('未找到指定的软件');
            }
        } catch (backupError) {
            console.error('备用数据也加载失败:', backupError);
            showErrorMessage('加载软件详情失败');
        }
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

// 渲染软件详情
function renderSoftwareDetail(software) {
    const detailContainer = document.getElementById('softwareDetail');
    const nameElement = document.getElementById('softwareName');
    
    if (nameElement) {
        nameElement.textContent = software.name;
    }
    
    if (detailContainer) {
        detailContainer.innerHTML = `
            <div class="detail-header">
                <img src="${software.image}" alt="${software.name}" class="detail-image" onerror="this.style.display='none'">
                <div class="detail-info">
                    <h1>${software.name}</h1>
                    <span class="software-type ${getTypeClass(software.type)}">${software.type}</span>
                    <p class="detail-description">${software.description}</p>
                </div>
            </div>
            <div class="detail-meta">
                <div class="meta-item">
                    <span class="meta-label">开源协议:</span>
                    <span>${software.license || '不适用'}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">使用范围:</span>
                    <span>${software.scope}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">功能分类:</span>
                    <span>${software.category}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">用户评分:</span>
                    <span>${software.rating || 0} / 5.0</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">使用手册:</span>
                    <a href="${software.manual || '#'}" class="document-link">查看手册</a>
                </div>
            </div>
            <div class="software-tags">
                ${software.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
        `;
    }
}

// 渲染版本信息
function renderVersions(versions) {
    const versionsList = document.getElementById('versionsList');
    if (!versionsList || !versions) return;

    versionsList.innerHTML = versions.map(version => `
        <div class="version-item">
            <div class="version-info">
                <h4>版本 ${version.version}</h4>
                <p class="version-description">${version.description}</p>
            </div>
            <div class="version-actions">
                <a href="${version.downloadUrl}" class="download-btn" onclick="handleDownload(event, '${version.version}')">下载</a>
            </div>
        </div>
    `).join('');
}

// 渲染文档列表
function renderDocuments(documents) {
    const documentsList = document.getElementById('documentsList');
    if (!documentsList) return;

    if (!documents || documents.length === 0) {
        documentsList.innerHTML = '<p>暂无相关文档</p>';
        return;
    }

    documentsList.innerHTML = documents.map(doc => `
        <div class="document-item">
            <div class="document-icon">📄</div>
            <div class="document-name">${doc}</div>
            <a href="#" class="document-link" onclick="viewDocument(event, '${doc}')">查看文档</a>
        </div>
    `).join('');
}

// 渲染评分
function renderRating(rating) {
    const ratingScore = document.getElementById('averageRating');
    const starsContainer = document.getElementById('starsContainer');
    
    if (ratingScore) {
        ratingScore.textContent = rating || 0;
    }
    
    if (starsContainer) {
        const fullStars = Math.floor(rating || 0);
        const halfStar = (rating || 0) % 1 >= 0.5 ? 1 : 0;
        const emptyStars = 5 - fullStars - halfStar;
        
        let stars = '';
        for (let i = 0; i < fullStars; i++) {
            stars += '★';
        }
        if (halfStar) {
            stars += '☆';
        }
        for (let i = 0; i < emptyStars; i++) {
            stars += '☆';
        }
        
        starsContainer.innerHTML = `<span style="color: #fbbf24;">${stars}</span>`;
    }
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

// 标签切换
function showTab(tabName, buttonElement) {
    // 移除所有活动状态
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabPanes.forEach(pane => pane.classList.remove('active'));
    
    // 设置当前标签为活动状态
    if (buttonElement) {
        buttonElement.classList.add('active');
    }
    document.getElementById(tabName).classList.add('active');
}

// 处理下载
function handleDownload(event, version) {
    event.preventDefault();
    if (currentSoftware) {
        alert(`开始下载 ${currentSoftware.name} 版本 ${version}\n\n注意：这是原型演示，实际下载功能需要后端支持。`);
    }
}

// 查看文档
function viewDocument(event, docName) {
    event.preventDefault();
    alert(`查看文档: ${docName}\n\n注意：这是原型演示，实际文档查看功能需要后端支持。`);
}

// 添加评价
function addReview() {
    const review = prompt('请输入您的评价内容:');
    if (review && review.trim()) {
        alert('感谢您的评价！\n\n注意：这是原型演示，实际评价功能需要后端支持。');
    }
}

// 显示错误信息
function showErrorMessage(message) {
    const mainContainer = document.querySelector('.main .container');
    if (mainContainer) {
        mainContainer.innerHTML = `
            <div style="text-align: center; padding: 40px; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                <h2 style="color: #ef4444; margin-bottom: 15px;">错误</h2>
                <p style="color: #666; margin-bottom: 20px;">${message}</p>
                <a href="index.html" style="display: inline-block; padding: 10px 20px; background: #2563eb; color: white; text-decoration: none; border-radius: 6px;">
                    返回软件列表
                </a>
            </div>
        `;
    }
}

// 监听浏览器后退按钮
window.addEventListener('popstate', function(event) {
    // 如果需要可以在这里处理后退逻辑
});
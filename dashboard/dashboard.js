// ============================================================
// DAE Product Price Analytics - Modern Interactive Dashboard
// Comprehensive Analytics, Comparison Engine & Visualizations
// ============================================================

(function () {
    'use strict';

    // Application State
    let rawDataset = [];
    let filteredDataset = [];
    let productSummary = [];
    let websiteSummary = [];

    let currentSortColumn = 'default';
    let currentSortOrder = 'asc';
    let currentPage = 1;
    let rowsPerPage = 25;
    let activeCompareProduct = 'Apple iPhone 15';

    // Chart.js Instances
    let trendChartInstance = null;
    let categoryChartInstance = null;
    let websiteChartInstance = null;
    let comparatorChartInstance = null;

    // DOM Elements
    const elements = {
        appSidebar: document.getElementById('appSidebar'),
        openSidebarBtn: document.getElementById('openSidebarBtn'),
        closeSidebarBtn: document.getElementById('closeSidebarBtn'),
        categoryFilter: document.getElementById('categoryFilter'),
        websiteFilter: document.getElementById('websiteFilter'),
        sortFilter: document.getElementById('sortFilter'),
        priceRangeFilter: document.getElementById('priceRangeFilter'),
        priceRangeValue: document.getElementById('priceRangeValue'),
        resetFiltersBtn: document.getElementById('resetFiltersBtn'),
        globalSearchInput: document.getElementById('globalSearchInput'),
        topBarRecordCount: document.getElementById('topBarRecordCount'),
        exportCsvBtn: document.getElementById('exportCsvBtn'),

        // KPIs
        kpiTotalRecords: document.getElementById('kpiTotalRecords'),
        kpiMinPrice: document.getElementById('kpiMinPrice'),
        kpiMinPriceProduct: document.getElementById('kpiMinPriceProduct'),
        kpiMinPriceSub: document.getElementById('kpiMinPriceSub'),
        kpiMaxPrice: document.getElementById('kpiMaxPrice'),
        kpiMaxPriceSub: document.getElementById('kpiMaxPriceSub'),
        kpiAvgPrice: document.getElementById('kpiAvgPrice'),
        kpiAvgRating: document.getElementById('kpiAvgRating'),
        kpiTotalReviews: document.getElementById('kpiTotalReviews'),
        kpiAvgDiscount: document.getElementById('kpiAvgDiscount'),
        kpiAvgSavings: document.getElementById('kpiAvgSavings'),

        // Comparator
        compareProductSelect: document.getElementById('compareProductSelect'),
        popularChipsContainer: document.getElementById('popularChipsContainer'),
        comparatorResultArea: document.getElementById('comparatorResultArea'),

        // Insights
        insightArbitrageTitle: document.getElementById('insightArbitrageTitle'),
        insightArbitrageDesc: document.getElementById('insightArbitrageDesc'),
        insightBestRetailerTitle: document.getElementById('insightBestRetailerTitle'),
        insightBestRetailerDesc: document.getElementById('insightBestRetailerDesc'),
        insightTopDealTitle: document.getElementById('insightTopDealTitle'),
        insightTopDealDesc: document.getElementById('insightTopDealDesc'),

        // Table & Pagination
        tableBody: document.getElementById('tableBody'),
        paginationInfo: document.getElementById('paginationInfo'),
        paginationControls: document.getElementById('paginationControls'),
        rowsPerPageSelect: document.getElementById('rowsPerPageSelect'),

        // Gallery & Lightbox
        galleryGrid: document.getElementById('matplotlibGalleryGrid'),
        lightboxModal: document.getElementById('lightboxModal'),
        lightboxImage: document.getElementById('lightboxImage'),
        lightboxTitle: document.getElementById('lightboxTitle'),
        lightboxDesc: document.getElementById('lightboxDesc'),
        lightboxCloseBtn: document.getElementById('lightboxCloseBtn'),
        lightboxBackdrop: document.getElementById('lightboxBackdrop'),
        lightboxDownloadBtn: document.getElementById('lightboxDownloadBtn'),

        toastContainer: document.getElementById('toastContainer')
    };

    // Chart.js Global Theme Customization
    if (window.Chart) {
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.font.family = "'Inter', sans-serif";
        Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.06)';
        Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(10, 13, 22, 0.94)';
        Chart.defaults.plugins.tooltip.titleFont = { family: "'Outfit', sans-serif", size: 13, weight: '700' };
        Chart.defaults.plugins.tooltip.bodyFont = { size: 12 };
        Chart.defaults.plugins.tooltip.padding = 12;
        Chart.defaults.plugins.tooltip.cornerRadius = 8;
        Chart.defaults.plugins.tooltip.borderColor = 'rgba(255, 255, 255, 0.12)';
        Chart.defaults.plugins.tooltip.borderWidth = 1;
    }

    // ============================================================
    // 1. INITIALIZATION & DATA LOADING
    // ============================================================
    document.addEventListener('DOMContentLoaded', async () => {
        initParticleCanvas();
        setupNavigationAndInteractions();
        setupTiltEffect();
        setupLightbox();

        try {
            // Load preprocessed datasets
            const [dataRes, prodRes, webRes] = await Promise.all([
                fetch('data.json'),
                fetch('product_summary.json'),
                fetch('website_summary.json')
            ]);

            rawDataset = await dataRes.json();
            productSummary = await prodRes.json();
            websiteSummary = await webRes.json();

            filteredDataset = [...rawDataset];

            // Initialize controls
            populateDropdownFilters();
            populateComparatorDropdown();
            bindFilterEvents();

            // Render all components
            refreshDashboard();
            renderPriceComparison(activeCompareProduct);
            showToast('⚡ Dataset initialized: 2,000 observations ready.');
        } catch (error) {
            console.error('Error loading dataset:', error);
            showToast('⚠️ Could not load data.json. Ensure local HTTP server is running.');
        }
    });

    // ============================================================
    // 2. PARTICLE CANVAS ANIMATION
    // ============================================================
    function initParticleCanvas() {
        const canvas = document.getElementById('particleCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let width = (canvas.width = window.innerWidth);
        let height = (canvas.height = window.innerHeight);

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        const particles = [];
        const particleCount = Math.min(Math.floor(width / 35), 45);

        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.5) * 0.4,
                radius: Math.random() * 1.5 + 0.5,
                alpha: Math.random() * 0.4 + 0.1
            });
        }

        function animate() {
            ctx.clearRect(0, 0, width, height);

            // Connect nearby particles
            for (let i = 0; i < particles.length; i++) {
                const p1 = particles[i];
                p1.x += p1.vx;
                p1.y += p1.vy;

                if (p1.x < 0) p1.x = width;
                if (p1.x > width) p1.x = 0;
                if (p1.y < 0) p1.y = height;
                if (p1.y > height) p1.y = 0;

                ctx.beginPath();
                ctx.arc(p1.x, p1.y, p1.radius, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(165, 180, 252, ${p1.alpha})`;
                ctx.fill();

                for (let j = i + 1; j < particles.length; j++) {
                    const p2 = particles[j];
                    const dx = p1.x - p2.x;
                    const dy = p1.y - p2.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 110) {
                        ctx.beginPath();
                        ctx.moveTo(p1.x, p1.y);
                        ctx.lineTo(p2.x, p2.y);
                        ctx.strokeStyle = `rgba(99, 102, 241, ${0.15 * (1 - dist / 110)})`;
                        ctx.lineWidth = 0.6;
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(animate);
        }
        animate();
    }

    // ============================================================
    // 3. UI CONTROLS & FILTERING
    // ============================================================
    function populateDropdownFilters() {
        const categories = [...new Set(rawDataset.map(item => item.Category))].sort();
        const websites = [...new Set(rawDataset.map(item => item.Website))].sort();

        categories.forEach(cat => {
            const opt = document.createElement('option');
            opt.value = cat;
            opt.textContent = cat;
            elements.categoryFilter.appendChild(opt);
        });

        websites.forEach(site => {
            const opt = document.createElement('option');
            opt.value = site;
            opt.textContent = site;
            elements.websiteFilter.appendChild(opt);
        });

        // Set max price limit on slider
        const maxObservedPrice = Math.max(...rawDataset.map(i => i['Selling Price (₹)']));
        elements.priceRangeFilter.max = Math.ceil(maxObservedPrice / 1000) * 1000;
        elements.priceRangeFilter.value = elements.priceRangeFilter.max;
        elements.priceRangeValue.textContent = formatRupee(elements.priceRangeFilter.max);
    }

    function populateComparatorDropdown() {
        const products = [...new Set(rawDataset.map(i => i['Product Name']))].sort();
        elements.compareProductSelect.innerHTML = '';

        products.forEach(p => {
            const opt = document.createElement('option');
            opt.value = p;
            opt.textContent = p;
            if (p === activeCompareProduct) opt.selected = true;
            elements.compareProductSelect.appendChild(opt);
        });
    }

    function bindFilterEvents() {
        elements.categoryFilter.addEventListener('change', applyFilters);
        elements.websiteFilter.addEventListener('change', applyFilters);
        elements.sortFilter.addEventListener('change', applyFilters);

        elements.priceRangeFilter.addEventListener('input', (e) => {
            elements.priceRangeValue.textContent = formatRupee(e.target.value);
            applyFilters();
        });

        let searchDebounce;
        elements.globalSearchInput.addEventListener('input', () => {
            clearTimeout(searchDebounce);
            searchDebounce = setTimeout(applyFilters, 150);
        });

        elements.resetFiltersBtn.addEventListener('click', () => {
            elements.categoryFilter.value = 'all';
            elements.websiteFilter.value = 'all';
            elements.sortFilter.value = 'default';
            elements.priceRangeFilter.value = elements.priceRangeFilter.max;
            elements.priceRangeValue.textContent = formatRupee(elements.priceRangeFilter.max);
            elements.globalSearchInput.value = '';
            applyFilters();
            showToast('🔄 All filters restored to default.');
        });

        // Rows per page
        elements.rowsPerPageSelect.addEventListener('change', (e) => {
            rowsPerPage = parseInt(e.target.value, 10);
            currentPage = 1;
            renderTable();
        });

        // Export CSV
        elements.exportCsvBtn.addEventListener('click', exportCurrentViewToCSV);

        // Comparator Selector
        elements.compareProductSelect.addEventListener('change', (e) => {
            activeCompareProduct = e.target.value;
            updateChipsActiveState(activeCompareProduct);
            renderPriceComparison(activeCompareProduct);
        });

        // Comparator Chips
        elements.popularChipsContainer.querySelectorAll('.chip-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const prod = btn.dataset.product;
                activeCompareProduct = prod;
                elements.compareProductSelect.value = prod;
                updateChipsActiveState(prod);
                renderPriceComparison(prod);
            });
        });

        // Gallery category tabs
        const tabBtns = document.querySelectorAll('.gallery-tab-btn');
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                tabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const cat = btn.dataset.filter;
                filterGalleryCards(cat);
            });
        });
    }

    function updateChipsActiveState(selectedProd) {
        elements.popularChipsContainer.querySelectorAll('.chip-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.product === selectedProd);
        });
    }

    function applyFilters() {
        const cat = elements.categoryFilter.value;
        const site = elements.websiteFilter.value;
        const maxPrice = parseFloat(elements.priceRangeFilter.value);
        const search = elements.globalSearchInput.value.trim().toLowerCase();

        filteredDataset = rawDataset.filter(item => {
            const matchCat = cat === 'all' || item.Category === cat;
            const matchSite = site === 'all' || item.Website === site;
            const matchPrice = item['Selling Price (₹)'] <= maxPrice;
            const matchSearch = !search ||
                item['Product Name'].toLowerCase().includes(search) ||
                item.Category.toLowerCase().includes(search) ||
                item.Website.toLowerCase().includes(search);

            return matchCat && matchSite && matchPrice && matchSearch;
        });

        // Sorting
        const sortVal = elements.sortFilter.value;
        if (sortVal === 'price_asc') {
            filteredDataset.sort((a, b) => a['Selling Price (₹)'] - b['Selling Price (₹)']);
        } else if (sortVal === 'price_desc') {
            filteredDataset.sort((a, b) => b['Selling Price (₹)'] - a['Selling Price (₹)']);
        } else if (sortVal === 'discount_desc') {
            filteredDataset.sort((a, b) => b['Discount (%)'] - a['Discount (%)']);
        } else if (sortVal === 'savings_desc') {
            filteredDataset.sort((a, b) => (b['Savings (₹)'] || 0) - (a['Savings (₹)'] || 0));
        } else if (sortVal === 'rating_desc') {
            filteredDataset.sort((a, b) => b['Rating'] - a['Rating']);
        } else if (sortVal === 'reviews_desc') {
            filteredDataset.sort((a, b) => b['Review Count'] - a['Review Count']);
        }

        currentPage = 1;
        refreshDashboard();
    }

    // ============================================================
    // 4. MAIN DASHBOARD REFRESH
    // ============================================================
    function refreshDashboard() {
        updateKPIs();
        updateSmartInsights();
        renderTrendChart();
        renderCategoryPriceChart();
        renderWebsiteComparisonChart();
        renderTable();

        elements.topBarRecordCount.textContent = filteredDataset.length.toLocaleString();
    }

    // ============================================================
    // 5. KPIS & AGGREGATIONS
    // ============================================================
    function updateKPIs() {
        const count = filteredDataset.length;

        if (count === 0) {
            elements.kpiTotalRecords.textContent = '0';
            elements.kpiMinPrice.textContent = '₹0';
            elements.kpiMinPriceProduct.textContent = 'No records match';
            elements.kpiMaxPrice.textContent = '₹0';
            elements.kpiAvgPrice.textContent = '₹0';
            elements.kpiAvgRating.textContent = '0.0 ★';
            elements.kpiAvgDiscount.textContent = '0%';
            return;
        }

        let minPrice = Infinity;
        let minProduct = null;
        let maxPrice = -Infinity;
        let maxProduct = null;
        let sumPrice = 0;
        let sumDiscount = 0;
        let sumRating = 0;
        let sumSavings = 0;
        let totalReviews = 0;

        filteredDataset.forEach(item => {
            const price = item['Selling Price (₹)'];
            sumPrice += price;
            sumDiscount += item['Discount (%)'] || 0;
            sumRating += item['Rating'] || 0;
            sumSavings += (item['Savings (₹)'] || 0);
            totalReviews += (item['Review Count'] || 0);

            if (price < minPrice) {
                minPrice = price;
                minProduct = item;
            }
            if (price > maxPrice) {
                maxPrice = price;
                maxProduct = item;
            }
        });

        const avgPrice = Math.round(sumPrice / count);
        const avgDiscount = (sumDiscount / count).toFixed(1);
        const avgRating = (sumRating / count).toFixed(2);
        const avgSavings = Math.round(sumSavings / count);

        // Animated counting
        animateCounter(elements.kpiTotalRecords, count);
        elements.kpiMinPrice.textContent = formatRupee(minPrice);
        elements.kpiMinPriceProduct.textContent = minProduct ? `${minProduct['Product Name']}` : '';
        elements.kpiMinPriceSub.textContent = minProduct ? `Available on ${minProduct.Website}` : '';

        elements.kpiMaxPrice.textContent = formatRupee(maxPrice);
        elements.kpiMaxPriceSub.textContent = maxProduct ? `${maxProduct['Product Name']} (${maxProduct.Website})` : '';

        elements.kpiAvgPrice.textContent = formatRupee(avgPrice);
        elements.kpiAvgRating.textContent = `${avgRating} ★`;
        elements.kpiTotalReviews.textContent = `${(totalReviews / 1000).toFixed(1)}k verified reviews`;

        elements.kpiAvgDiscount.textContent = `${avgDiscount}%`;
        elements.kpiAvgSavings.textContent = `Avg saving: ${formatRupee(avgSavings)} / item`;
    }

    function animateCounter(element, targetValue) {
        const start = parseInt(element.textContent.replace(/,/g, ''), 10) || 0;
        const duration = 500;
        const startTime = performance.now();

        function step(now) {
            const progress = Math.min((now - startTime) / duration, 1);
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.round(start + (targetValue - start) * easeOut);
            element.textContent = current.toLocaleString();

            if (progress < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }

    // ============================================================
    // 6. SMART MARKET INSIGHTS
    // ============================================================
    function updateSmartInsights() {
        if (!productSummary || productSummary.length === 0) return;

        // Calculate biggest spread
        let maxSpread = 0;
        let spreadProduct = null;

        productSummary.forEach(p => {
            const spread = p['Worst Price'] - p['Best Price'];
            if (spread > maxSpread) {
                maxSpread = spread;
                spreadProduct = p;
            }
        });

        if (spreadProduct) {
            const spreadPct = ((maxSpread / spreadProduct['Best Price']) * 100).toFixed(1);
            elements.insightArbitrageTitle.textContent = `${spreadProduct['Product Name']} Price Disparity`;
            elements.insightArbitrageDesc.innerHTML = `
                The <strong>${spreadProduct['Product Name']}</strong> varies from <strong>${formatRupee(spreadProduct['Best Price'])}</strong> to <strong>${formatRupee(spreadProduct['Worst Price'])}</strong> across retailers. 
                Savvy consumers save up to <strong>${formatRupee(maxSpread)} (${spreadPct}%)</strong> simply by selecting the optimal store!
            `;
        }

        // Best retailer for discount
        if (websiteSummary && websiteSummary.length > 0) {
            const sortedByDisc = [...websiteSummary].sort((a, b) => b['Avg Discount'] - a['Avg Discount']);
            const topSite = sortedByDisc[0];
            const lowestSite = sortedByDisc[sortedByDisc.length - 1];

            elements.insightBestRetailerTitle.textContent = `${topSite.Website} Leads in Promotional Depth`;
            elements.insightBestRetailerDesc.innerHTML = `
                Across all categories, <strong>${topSite.Website}</strong> provides the steepest average discount at <strong>${topSite['Avg Discount'].toFixed(2)}%</strong>, 
                beating out ${lowestSite.Website} (${lowestSite['Avg Discount'].toFixed(2)}%) by ${(topSite['Avg Discount'] - lowestSite['Avg Discount']).toFixed(1)} percentage points.
            `;
        }
    }

    // ============================================================
    // 7. INTERACTIVE PRICE COMPARATOR ENGINE
    // ============================================================
    function renderPriceComparison(productName) {
        const matchingRows = rawDataset.filter(i => i['Product Name'] === productName);
        if (matchingRows.length === 0) {
            elements.comparatorResultArea.innerHTML = `<p class="comparison-placeholder">No pricing observations for ${productName}</p>`;
            return;
        }

        // Aggregate by Website
        const siteAverages = {};
        matchingRows.forEach(item => {
            const site = item.Website;
            if (!siteAverages[site]) {
                siteAverages[site] = {
                    sum: 0,
                    count: 0,
                    mrp: item['MRP (₹)'],
                    rating: item.Rating,
                    reviews: item['Review Count'],
                    category: item.Category
                };
            }
            siteAverages[site].sum += item['Selling Price (₹)'];
            siteAverages[site].count += 1;
        });

        const comparisonData = Object.entries(siteAverages).map(([site, data]) => {
            const avgPrice = Math.round(data.sum / data.count);
            const discount = Math.round(((data.mrp - avgPrice) / data.mrp) * 1000) / 10;
            return {
                website: site,
                price: avgPrice,
                mrp: data.mrp,
                discount: discount,
                rating: data.rating,
                reviews: data.reviews,
                category: data.category
            };
        });

        // Sort from lowest price to highest
        comparisonData.sort((a, b) => a.price - b.price);

        const bestDeal = comparisonData[0];
        const worstDeal = comparisonData[comparisonData.length - 1];
        const spreadAmount = worstDeal.price - bestDeal.price;
        const savingsPct = Math.round((spreadAmount / worstDeal.price) * 100);

        // Render HTML
        elements.comparatorResultArea.innerHTML = `
            <div class="compare-winner-banner">
                <div class="winner-badge-strip">
                    <span class="winner-icon">🏆</span>
                    <div>
                        <div class="winner-subtitle">RECOMMENDED PURCHASE LOCATION</div>
                        <h4 class="winner-title">${bestDeal.website} offers the lowest price for ${productName}</h4>
                    </div>
                </div>
                <div class="winner-price-callout">
                    <div class="winner-price-val">${formatRupee(bestDeal.price)}</div>
                    <div class="winner-savings-pill">Save ${formatRupee(spreadAmount)} (${savingsPct}% cheaper than ${worstDeal.website})</div>
                </div>
            </div>

            <div class="comparator-retailers-grid">
                ${comparisonData.map((item, idx) => {
                    const isCheapest = idx === 0;
                    const diff = item.price - bestDeal.price;
                    const dotClass = getRetailerDotClass(item.website);

                    return `
                        <div class="retailer-price-card ${isCheapest ? 'is-cheapest' : ''}">
                            <div class="retailer-card-header">
                                <div class="site-badge">
                                    <span class="site-dot ${dotClass}"></span>
                                    <span class="retailer-name">${item.website}</span>
                                </div>
                                ${isCheapest
                                    ? '<span class="retailer-tag tag-best">Best Deal</span>'
                                    : `<span class="retailer-tag tag-diff">+${formatRupee(diff)}</span>`
                                }
                            </div>
                            <div class="retailer-price">${formatRupee(item.price)}</div>
                            <div class="retailer-card-meta">
                                <span>MRP <strike>${formatRupee(item.mrp)}</strike></span>
                                <span class="discount-pill">${item.discount}% off</span>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>

            <div class="canvas-holder" style="height: 220px; margin-top: 0.5rem;">
                <canvas id="comparatorBarChart"></canvas>
            </div>
        `;

        // Render Horizontal Bar Chart for Comparator
        const ctx = document.getElementById('comparatorBarChart').getContext('2d');
        if (comparatorChartInstance) comparatorChartInstance.destroy();

        const labels = comparisonData.map(d => d.website);
        const prices = comparisonData.map(d => d.price);
        const backgroundColors = comparisonData.map((d, i) => i === 0 ? '#10b981' : '#6366f1');

        comparatorChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Selling Price (₹)',
                    data: prices,
                    backgroundColor: backgroundColors,
                    borderRadius: 6,
                    barThickness: 20
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => ` Price: ₹${ctx.parsed.x.toLocaleString()}`
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.04)' },
                        ticks: { callback: v => '₹' + (v / 1000).toFixed(0) + 'k' }
                    },
                    y: {
                        grid: { display: false }
                    }
                }
            }
        });
    }

    function getRetailerDotClass(website) {
        const lower = website.toLowerCase();
        if (lower.includes('amazon')) return 'amazon';
        if (lower.includes('flipkart')) return 'flipkart';
        if (lower.includes('croma')) return 'croma';
        if (lower.includes('reliance')) return 'reliance';
        return 'vijay';
    }

    // ============================================================
    // 8. CHART.JS VISUALIZATIONS
    // ============================================================
    // --- Chart 1: Time Series Trend Line Chart ---
    function renderTrendChart() {
        const canvas = document.getElementById('dynamicTrendChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (trendChartInstance) trendChartInstance.destroy();

        // Get unique products in filtered selection (max 4 lines for clarity)
        const productsInSelection = [...new Set(filteredDataset.map(i => i['Product Name']))];
        const selectedProducts = productsInSelection.slice(0, 4);

        const allDates = [...new Set(filteredDataset.map(i => i['Scrape Date']))].sort();

        const colors = [
            { border: '#6366f1', fill: 'rgba(99, 102, 241, 0.15)' },
            { border: '#10b981', fill: 'rgba(16, 185, 129, 0.15)' },
            { border: '#ec4899', fill: 'rgba(236, 72, 153, 0.15)' },
            { border: '#06b6d4', fill: 'rgba(6, 182, 212, 0.15)' }
        ];

        const datasets = selectedProducts.map((prodName, idx) => {
            const productRecords = filteredDataset.filter(i => i['Product Name'] === prodName);
            const dateMap = {};

            productRecords.forEach(r => {
                const date = r['Scrape Date'];
                if (!dateMap[date]) dateMap[date] = { sum: 0, count: 0 };
                dateMap[date].sum += r['Selling Price (₹)'];
                dateMap[date].count += 1;
            });

            const dataPoints = allDates.map(d => {
                return dateMap[d] ? Math.round(dateMap[d].sum / dateMap[d].count) : null;
            });

            const col = colors[idx % colors.length];

            return {
                label: prodName,
                data: dataPoints,
                borderColor: col.border,
                backgroundColor: col.fill,
                borderWidth: 2.5,
                pointRadius: 3,
                pointHoverRadius: 6,
                pointBackgroundColor: col.border,
                tension: 0.35,
                fill: idx === 0, // Gradient fill on top product
                spanGaps: true
            };
        });

        trendChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: allDates,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            boxWidth: 8,
                            padding: 15,
                            font: { size: 11, family: "'Inter', sans-serif" }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => ` ${ctx.dataset.label}: ₹${ctx.parsed.y.toLocaleString()}`
                        }
                    }
                },
                scales: {
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.04)' },
                        ticks: {
                            callback: (v) => '₹' + (v / 1000).toFixed(0) + 'k'
                        }
                    },
                    x: {
                        grid: { display: false },
                        ticks: {
                            maxTicksLimit: 10,
                            font: { size: 10 }
                        }
                    }
                }
            }
        });
    }

    // --- Chart 2: Category Average Price Bar Chart ---
    function renderCategoryPriceChart() {
        const canvas = document.getElementById('dynamicCategoryChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (categoryChartInstance) categoryChartInstance.destroy();

        const catAgg = {};
        filteredDataset.forEach(i => {
            if (!catAgg[i.Category]) catAgg[i.Category] = { sum: 0, count: 0 };
            catAgg[i.Category].sum += i['Selling Price (₹)'];
            catAgg[i.Category].count += 1;
        });

        const entries = Object.entries(catAgg).map(([cat, val]) => ({
            cat,
            avg: Math.round(val.sum / val.count)
        })).sort((a, b) => b.avg - a.avg);

        const labels = entries.map(e => e.cat);
        const values = entries.map(e => e.avg);
        const palette = ['#6366f1', '#ec4899', '#14b8a6', '#f59e0b', '#8b5cf6', '#06b6d4', '#10b981'];

        categoryChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Avg Price',
                    data: values,
                    backgroundColor: palette.slice(0, labels.length),
                    borderRadius: 6,
                    barThickness: 22
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => ` Avg: ₹${ctx.parsed.x.toLocaleString()}`
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.04)' },
                        ticks: { callback: v => '₹' + (v / 1000).toFixed(0) + 'k' }
                    },
                    y: { grid: { display: false } }
                }
            }
        });
    }

    // --- Chart 3: Website Competitiveness (Min, Avg, Max) ---
    function renderWebsiteComparisonChart() {
        const canvas = document.getElementById('dynamicWebsiteChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (websiteChartInstance) websiteChartInstance.destroy();

        const siteAgg = {};
        filteredDataset.forEach(i => {
            const s = i.Website;
            if (!siteAgg[s]) siteAgg[s] = { min: Infinity, max: -Infinity, sum: 0, count: 0 };
            const p = i['Selling Price (₹)'];
            siteAgg[s].sum += p;
            siteAgg[s].count += 1;
            if (p < siteAgg[s].min) siteAgg[s].min = p;
            if (p > siteAgg[s].max) siteAgg[s].max = p;
        });

        const sites = Object.keys(siteAgg).sort();
        const minPrices = sites.map(s => siteAgg[s].min);
        const avgPrices = sites.map(s => Math.round(siteAgg[s].sum / siteAgg[s].count));
        const maxPrices = sites.map(s => siteAgg[s].max);

        websiteChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: sites,
                datasets: [
                    { label: 'Best Price', data: minPrices, backgroundColor: '#10b981', borderRadius: 4 },
                    { label: 'Average Price', data: avgPrices, backgroundColor: '#6366f1', borderRadius: 4 },
                    { label: 'Worst Price', data: maxPrices, backgroundColor: '#f43f5e', borderRadius: 4 }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { usePointStyle: true, boxWidth: 8, padding: 12, font: { size: 10 } }
                    },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => ` ${ctx.dataset.label}: ₹${ctx.parsed.y.toLocaleString()}`
                        }
                    }
                },
                scales: {
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.04)' },
                        ticks: { callback: v => '₹' + (v / 1000).toFixed(0) + 'k' }
                    },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    // ============================================================
    // 9. PRODUCT EXPLORER DATA TABLE WITH PAGINATION
    // ============================================================
    function renderTable() {
        const totalItems = filteredDataset.length;
        const totalPages = Math.ceil(totalItems / rowsPerPage) || 1;

        if (currentPage > totalPages) currentPage = totalPages;

        const startIdx = (currentPage - 1) * rowsPerPage;
        const endIdx = Math.min(startIdx + rowsPerPage, totalItems);
        const pageItems = filteredDataset.slice(startIdx, endIdx);

        elements.tableBody.innerHTML = '';

        if (pageItems.length === 0) {
            elements.tableBody.innerHTML = `
                <tr>
                    <td colspan="10" style="text-align:center; padding: 2.5rem; color: var(--text-muted);">
                        No products match your current filters. Try resetting the filters.
                    </td>
                </tr>
            `;
            elements.paginationInfo.textContent = 'Showing 0 of 0 entries';
            elements.paginationControls.innerHTML = '';
            return;
        }

        pageItems.forEach((item, index) => {
            const overallIndex = startIdx + index + 1;
            const dotClass = getRetailerDotClass(item.Website);
            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td><span style="color:var(--text-muted); font-size: 0.78rem;">#${overallIndex}</span></td>
                <td><strong>${highlightSearch(item['Product Name'])}</strong></td>
                <td><span class="table-badge">${item.Category}</span></td>
                <td>
                    <span class="site-badge">
                        <span class="site-dot ${dotClass}"></span>
                        ${item.Website}
                    </span>
                </td>
                <td style="color:var(--text-secondary); font-size: 0.8rem;">${item['Scrape Date']}</td>
                <td class="price-strikethrough">${formatRupee(item['MRP (₹)'])}</td>
                <td class="price-highlight">${formatRupee(item['Selling Price (₹)'])}</td>
                <td class="discount-pill">${item['Discount (%)']}%</td>
                <td class="rating-pill">⭐ ${item.Rating}</td>
                <td>
                    <button class="table-btn-compare" data-product="${item['Product Name']}">Compare</button>
                </td>
            `;

            elements.tableBody.appendChild(tr);
        });

        // Bind quick compare buttons
        elements.tableBody.querySelectorAll('.table-btn-compare').forEach(btn => {
            btn.addEventListener('click', () => {
                const prod = btn.dataset.product;
                activeCompareProduct = prod;
                elements.compareProductSelect.value = prod;
                updateChipsActiveState(prod);
                renderPriceComparison(prod);

                // Smooth scroll to comparison section
                const target = document.getElementById('compareTool');
                if (target) target.scrollIntoView({ behavior: 'smooth' });
                showToast(`🔍 Loaded ${prod} in Price Comparator.`);
            });
        });

        // Update Pagination Controls
        elements.paginationInfo.textContent = `Showing ${startIdx + 1} to ${endIdx} of ${totalItems.toLocaleString()} entries`;
        renderPaginationButtons(totalPages);
    }

    function renderPaginationButtons(totalPages) {
        elements.paginationControls.innerHTML = '';

        const prevBtn = document.createElement('button');
        prevBtn.className = 'page-btn';
        prevBtn.textContent = '‹';
        prevBtn.disabled = currentPage === 1;
        prevBtn.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                renderTable();
            }
        });
        elements.paginationControls.appendChild(prevBtn);

        // Compute page numbers to display
        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(totalPages, startPage + 4);
        if (endPage - startPage < 4) startPage = Math.max(1, endPage - 4);

        for (let p = startPage; p <= endPage; p++) {
            const pageBtn = document.createElement('button');
            pageBtn.className = `page-btn ${p === currentPage ? 'active' : ''}`;
            pageBtn.textContent = p;
            pageBtn.addEventListener('click', () => {
                currentPage = p;
                renderTable();
            });
            elements.paginationControls.appendChild(pageBtn);
        }

        const nextBtn = document.createElement('button');
        nextBtn.className = 'page-btn';
        nextBtn.textContent = '›';
        nextBtn.disabled = currentPage === totalPages;
        nextBtn.addEventListener('click', () => {
            if (currentPage < totalPages) {
                currentPage++;
                renderTable();
            }
        });
        elements.paginationControls.appendChild(nextBtn);
    }

    function highlightSearch(text) {
        const query = elements.globalSearchInput.value.trim();
        if (!query) return text;
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark style="background: rgba(99,102,241,0.3); color:#fff; border-radius:2px;">$1</mark>');
    }

    // ============================================================
    // 10. MATPLOTLIB GALLERY & LIGHTBOX
    // ============================================================
    function filterGalleryCards(category) {
        const cards = elements.galleryGrid.querySelectorAll('.gallery-card');
        cards.forEach(card => {
            const cardCat = card.dataset.category || '';
            if (category === 'all' || cardCat.includes(category)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    }

    function setupLightbox() {
        const cards = document.querySelectorAll('.gallery-card');
        cards.forEach(card => {
            card.addEventListener('click', () => {
                const imgUrl = card.dataset.img;
                const title = card.dataset.title;
                const desc = card.dataset.desc;

                elements.lightboxImage.src = imgUrl;
                elements.lightboxTitle.textContent = title;
                elements.lightboxDesc.textContent = desc;
                elements.lightboxDownloadBtn.onclick = () => {
                    const link = document.createElement('a');
                    link.href = imgUrl;
                    link.download = imgUrl.split('/').pop();
                    link.click();
                };

                elements.lightboxModal.classList.add('active');
            });
        });

        elements.lightboxCloseBtn.addEventListener('click', closeLightbox);
        elements.lightboxBackdrop.addEventListener('click', closeLightbox);

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && elements.lightboxModal.classList.contains('active')) {
                closeLightbox();
            }
            // Shortcut '/' for search
            if (e.key === '/' && document.activeElement !== elements.globalSearchInput) {
                e.preventDefault();
                elements.globalSearchInput.focus();
            }
        });
    }

    function closeLightbox() {
        elements.lightboxModal.classList.remove('active');
    }

    // ============================================================
    // 11. NAVIGATION & MICRO-INTERACTIONS
    // ============================================================
    function setupNavigationAndInteractions() {
        // Mobile Sidebar Drawer
        if (elements.openSidebarBtn && elements.appSidebar) {
            elements.openSidebarBtn.addEventListener('click', () => {
                elements.appSidebar.classList.add('open');
            });
        }
        if (elements.closeSidebarBtn && elements.appSidebar) {
            elements.closeSidebarBtn.addEventListener('click', () => {
                elements.appSidebar.classList.remove('open');
            });
        }

        // Active navigation link highlighting on scroll
        const navLinks = document.querySelectorAll('.nav-item');
        const sections = document.querySelectorAll('.dashboard-block, .hero-section');

        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').replace('#', '');
                const targetEl = document.getElementById(targetId);
                if (targetEl) {
                    targetEl.scrollIntoView({ behavior: 'smooth' });
                    navLinks.forEach(l => l.classList.remove('active'));
                    link.classList.add('active');
                }
                if (window.innerWidth <= 1024) {
                    elements.appSidebar.classList.remove('open');
                }
            });
        });

        // Intersection observer for section spying
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.id;
                    navLinks.forEach(link => {
                        link.classList.toggle('active', link.dataset.target === id);
                    });
                }
            });
        }, { threshold: 0.3 });

        sections.forEach(s => observer.observe(s));
    }

    // 3D Perspective Tilt on KPI Cards
    function setupTiltEffect() {
        const tiltCards = document.querySelectorAll('.tilt-card');
        tiltCards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = ((y - centerY) / centerY) * -7;
                const rotateY = ((x - centerX) / centerX) * 7;

                card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg) translateY(0px)';
            });
        });
    }

    // Export CSV utility
    function exportCurrentViewToCSV() {
        if (!filteredDataset || filteredDataset.length === 0) {
            showToast('⚠️ No data to export.');
            return;
        }

        const headers = ['Product Name', 'Category', 'Website', 'Scrape Date', 'MRP (₹)', 'Selling Price (₹)', 'Discount (%)', 'Rating', 'Review Count', 'Savings (₹)'];
        const csvRows = [headers.join(',')];

        filteredDataset.forEach(row => {
            const values = [
                `"${(row['Product Name'] || '').replace(/"/g, '""')}"`,
                `"${row.Category || ''}"`,
                `"${row.Website || ''}"`,
                `"${row['Scrape Date'] || ''}"`,
                row['MRP (₹)'] || 0,
                row['Selling Price (₹)'] || 0,
                row['Discount (%)'] || 0,
                row['Rating'] || 0,
                row['Review Count'] || 0,
                row['Savings (₹)'] || 0
            ];
            csvRows.push(values.join(','));
        });

        const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `DAE_Price_Analytics_Export_${new Date().toISOString().slice(0, 10)}.csv`;
        a.click();
        URL.revokeObjectURL(url);
        showToast(`📥 Exported ${filteredDataset.length.toLocaleString()} rows to CSV.`);
    }

    // Toast Notification System
    function showToast(message) {
        if (!elements.toastContainer) return;
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        elements.toastContainer.appendChild(toast);

        setTimeout(() => {
            if (toast.parentNode) toast.parentNode.removeChild(toast);
        }, 4000);
    }

    // Utility: Format numbers as Indian Rupees (₹)
    function formatRupee(val) {
        if (val === null || val === undefined || isNaN(val)) return '₹0';
        return '₹' + Math.round(val).toLocaleString('en-IN');
    }

})();

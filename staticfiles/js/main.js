// Bright Edu Consultancy Interactive Scripts

document.addEventListener('DOMContentLoaded', function () {
    // 1. Mobile Menu Toggle
    const mobileMenuButton = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // 2. WeChat Modal Toggle
    const wechatModal = document.getElementById('wechat-modal');
    const wechatTriggers = document.querySelectorAll('.trigger-wechat-modal');
    const closeWechatBtn = document.getElementById('close-wechat-modal');

    if (wechatModal) {
        wechatTriggers.forEach(btn => {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                wechatModal.classList.remove('hidden');
                wechatModal.classList.add('flex');
            });
        });

        if (closeWechatBtn) {
            closeWechatBtn.addEventListener('click', function () {
                wechatModal.classList.add('hidden');
                wechatModal.classList.remove('flex');
            });
        }

        // Close on background click
        wechatModal.addEventListener('click', function (e) {
            if (e.target === wechatModal) {
                wechatModal.classList.add('hidden');
                wechatModal.classList.remove('flex');
            }
        });
    }

    // 3. Copy WeChat ID to Clipboard
    const copyWechatBtn = document.getElementById('copy-wechat-btn');
    if (copyWechatBtn) {
        copyWechatBtn.addEventListener('click', function () {
            const wechatId = this.getAttribute('data-wechat-id') || 'BrightEdu_China';
            navigator.clipboard.writeText(wechatId).then(() => {
                const originalText = this.innerText;
                this.innerText = 'Copied to Clipboard! ✓';
                this.classList.add('bg-emerald-600', 'text-white');
                setTimeout(() => {
                    this.innerText = originalText;
                    this.classList.remove('bg-emerald-600', 'text-white');
                }, 2500);
            });
        });
    }

    // 4. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-box');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.6s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 600);
        }, 6000);
    });
});

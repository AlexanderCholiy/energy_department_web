document.addEventListener("DOMContentLoaded", function() {
    const sideMenu = document.getElementById("sideMenu");
    const mainContent = document.getElementById("mainContent");
    const sideMenuButton = document.getElementById("sidemenuButton");

    function getCookie(name) {
        const value = document.cookie;
        const parts = value.split('; ' + name + '=');
        return parts.length === 2 ? parts.pop().split(';').shift() : null;
    }

    const isCollapsed = getCookie("sideMenuCollapsed") === "true";
    sideMenu.classList.toggle("collapsed", isCollapsed);
    mainContent.style.marginLeft = isCollapsed ? "30px" : "200px";

    // Загрузим состояние подменю
    const submenuStates = getCookie("submenuStates");
    if (submenuStates) {
        const states = JSON.parse(submenuStates);
        for (const [id, isActive] of Object.entries(states)) {
            const submenu = document.getElementById(id);
            if (submenu) {
                // Открываем подменю только если боковое меню не скрыто
                if (!isCollapsed) {
                    submenu.classList.toggle('active', isActive);
                }
            }
        }
    }

    sideMenuButton.addEventListener("click", function() {
        const isCurrentlyCollapsed = sideMenu.classList.toggle("collapsed");
        mainContent.style.marginLeft = isCurrentlyCollapsed ? "30px" : "200px";
        document.cookie = `sideMenuCollapsed=${isCurrentlyCollapsed}; path=/`;
        if (isCurrentlyCollapsed) closeAllSubmenus();
    });

    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            toggleSubmenu(this);
        });
    });

    function toggleSubmenu(item) {
        const targetId = item.getAttribute('data-target');
        const submenu = document.getElementById(targetId);
        
        // Проверяем, скрыто ли боковое меню
        if (sideMenu.classList.contains('collapsed')) {
            // Если боковое меню скрыто, сначала раскрываем его
            sideMenu.classList.remove('collapsed');
            mainContent.style.marginLeft = "200px"; 
            document.cookie = "sideMenuCollapsed=false; path=/"; 

            // Ждем, чтобы дать время на анимацию, а затем открываем подменю
            setTimeout(() => {
                submenu.classList.toggle('active');
                saveSubmenuState(targetId, submenu.classList.contains('active'));
            }, 300); // Задержка, чтобы дать время на анимацию
        } else {
            // Если боковое меню открыто, просто открываем подменю
            submenu.classList.toggle('active');
            saveSubmenuState(targetId, submenu.classList.contains('active'));
        }
    }

    function saveSubmenuState(id, isActive) {
        const submenuStates = getCookie("submenuStates");
        let states = submenuStates ? JSON.parse(submenuStates) : {};
        states[id] = isActive;
        document.cookie = `submenuStates=${JSON.stringify(states)}; path=/`;
    }

    function closeAllSubmenus() {
        document.querySelectorAll('.submenu').forEach(sub => {
            sub.classList.remove('active');
        });
    }
});

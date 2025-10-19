// static/script.js

document.addEventListener('DOMContentLoaded', function() {
    const toggleModeButton = document.getElementById('toggle-mode');
    const toggleViewButton = document.getElementById('toggle-view');
    let isDarkMode = localStorage.getItem('isDarkMode') === 'true';
    let isMobileView = localStorage.getItem('isMobileView') === 'true';

    // Aplica as preferências salvas
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        if (toggleModeButton) toggleModeButton.innerText = 'Modo Claro';
    }

    if (isMobileView) {
        document.body.classList.add('mobile-view');
        if (toggleViewButton) toggleViewButton.innerText = 'Versão Web';
    }

    // ====== Atualização de sensores (mantido) ======
    function updateData() {
        fetch('/get_sensor_data')
            .then(response => response.json())
            .then(data => {
                const byId = id => document.getElementById(id);
                if (byId('temp'))       byId('temp').innerHTML       = data.temperature + ' &deg;C';
                if (byId('hum'))        byId('hum').innerHTML        = data.humidity + ' %';
                if (byId('distance'))   byId('distance').innerHTML   = data.distance + ' cm';
                if (byId('led1_pwm'))   byId('led1_pwm').innerHTML   = data.led1_pwm + ' %';
                if (byId('led2_pwm'))   byId('led2_pwm').innerHTML   = data.led2_pwm + ' %';
                if (byId('led3_pwm'))   byId('led3_pwm').innerHTML   = data.led3_pwm + ' %';
                if (byId('ldrValue'))   byId('ldrValue').innerHTML   = data.ldr_value + ' *';
            })
            .catch(error => console.error('Erro ao obter dados do sensor:', error));
    }
    setInterval(updateData, 2000);
    updateData();

    // ====== Alternar entre modo claro e escuro (mantido) ======
    if (toggleModeButton) {
        toggleModeButton.addEventListener('click', function() {
            if (isDarkMode) {
                document.body.classList.remove('dark-mode');
                toggleModeButton.innerText = 'Modo Escuro';
            } else {
                document.body.classList.add('dark-mode');
                toggleModeButton.innerText = 'Modo Claro';
            }
            isDarkMode = !isDarkMode;
            localStorage.setItem('isDarkMode', isDarkMode);
        });
    }

    // ====== Alternar entre versão mobile e web (mantido) ======
    if (toggleViewButton) {
        toggleViewButton.addEventListener('click', function() {
            if (isMobileView) {
                document.body.classList.remove('mobile-view');
                toggleViewButton.innerText = 'Versão Mobile';
            } else {
                document.body.classList.add('mobile-view');
                toggleViewButton.innerText = 'Versão Web';
            }
            isMobileView = !isMobileView;
            localStorage.setItem('isMobileView', isMobileView);
        });
    }

    // ====== Listagem de Peças: reaproveita a mesma estrutura/IDs do template ======
    (function initListaPecasFiltro() {
        const input = document.getElementById('meshFile');     // mesmo id reaproveitado
        const btn   = document.getElementById('btnCalcular');  // mesmo id reaproveitado
        const lista = document.getElementById('listaPecas');

        if (!input || !btn || !lista) return; // página sem listagem; não faz nada

        const widthEl  = document.getElementById('widthValue');   // total (filtrado)
        const depthEl  = document.getElementById('depthValue');   // ativas (filtrado)
        const heightEl = document.getElementById('heightValue');  // preço médio (filtrado)

        function filtrarPecas() {
            const termo = (input.value || '').toLowerCase().trim();
            const itens = lista.querySelectorAll('.pecaitem');

            let visiveis = 0;
            let ativas = 0;
            let somaPrecos = 0;
            let contaPrecos = 0;

            itens.forEach(li => {
                const alvo = (li.getAttribute('data-search') || '').toLowerCase();
                const show = !termo || alvo.includes(termo);
                li.style.display = show ? '' : 'none';

                if (show) {
                    visiveis++;
                    // ativo? usar atributo data-ativo="1" se você quiser; 
                    // aqui inferimos pelo badge/Conteúdo, então melhor marcar no server:
                    // <li ... data-ativo="{{ 1 if p.ativo else 0 }}" data-preco="{{ p.preco or '' }}">
                    const ativo = li.getAttribute('data-ativo');
                    if (ativo === '1') ativas++;

                    const precoStr = li.getAttribute('data-preco');
                    if (precoStr && !isNaN(precoStr)) {
                        somaPrecos += parseFloat(precoStr);
                        contaPrecos++;
                    }
                }
            });

            // Atualiza os 3 indicadores mantendo IDs
            if (widthEl)  widthEl.textContent  = String(visiveis);
            if (depthEl)  depthEl.textContent  = String(ativas);
            if (heightEl) heightEl.textContent = contaPrecos ? (somaPrecos / contaPrecos).toFixed(2) : '0.00';
        }

        btn.addEventListener('click', filtrarPecas);
        input.addEventListener('keyup', (e) => { if (e.key === 'Enter') filtrarPecas(); });

        // Filtro inicial (mostra totais baseados no estado atual da lista)
        filtrarPecas();
    })();
});

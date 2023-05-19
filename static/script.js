window.addEventListener('scroll', function() {
    var tableHeader = document.querySelector('thead');
    var rect = tableHeader.getBoundingClientRect();
    
    if (rect.top <= 0) {
        tableHeader.classList.add('sticky');
    } else {
        tableHeader.classList.remove('sticky');
    }
});

window.addEventListener('DOMContentLoaded', function() {
    var arbitrageCells = document.querySelectorAll('td.arbitrage');

    arbitrageCells.forEach(function(cell) {
        var arbitrage = parseFloat(cell.textContent);
        
        if (arbitrage >= 1 && arbitrage <= 20) {
            cell.classList.add('highlight-green');
        } else if (arbitrage >= -20 && arbitrage <= -1) {
            cell.classList.add('highlight-red');
        }
    });
});
window.addEventListener('DOMContentLoaded', function() {
    var arrowKey = document.getElementById('arrow-key');
    var greenCells = document.querySelectorAll('td.highlight-green');
    var redCells = document.querySelectorAll('td.highlight-red');

    var currentIndex = -1;
    var clickCount = 0;

    arrowKey.addEventListener('click', function() {
        clickCount++;

        if (clickCount === 1) {
            if (currentIndex === -1 || currentIndex === greenCells.length - 1) {
                currentIndex = 0;
            } else {
                currentIndex++;
            }

            if (greenCells.length > 0) {
                greenCells.forEach(function(cell) {
                    cell.classList.remove('current');
                });

                greenCells[currentIndex].classList.add('current');
                greenCells[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        } else if (clickCount === 2) {
            if (currentIndex === -1 || currentIndex === redCells.length - 1) {
                currentIndex = 0;
            } else {
                currentIndex++;
            }

            if (redCells.length > 0) {
                redCells.forEach(function(cell) {
                    cell.classList.remove('current');
                });

                redCells[currentIndex].classList.add('current');
                redCells[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        } else {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            clickCount = 0;
        }
    });
});

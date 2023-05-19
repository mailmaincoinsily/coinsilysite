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
  var arbitrageRows = document.querySelectorAll('tbody tr');

  arbitrageRows.forEach(function(row) {
    var arbitrageCell = row.querySelector('.arbitrage');
    var arbitrage = parseFloat(arbitrageCell.textContent);

    if (arbitrage >= 1 && arbitrage <= 20) {
      row.classList.add('highlight-green');
    } else if (arbitrage >= -20 && arbitrage <= -1) {
      row.classList.add('highlight-red');
    }
  });
});

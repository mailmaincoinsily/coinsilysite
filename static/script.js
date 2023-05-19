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
        
        if ((arbitrage >= 1 && arbitrage <= 20) || (arbitrage >= -20 && arbitrage <= -1)) {
            cell.classList.add('highlight');
        }
    });
});

window.addEventListener('DOMContentLoaded', function() {
  var arrow = document.createElement('div');
  arrow.className = 'floating-arrow';
  document.body.appendChild(arrow);

  var highlightedCells = [];
  var currentIndex = -1;

  arrow.addEventListener('click', function() {
    if (highlightedCells.length > 0) {
      if (currentIndex === -1 || currentIndex >= highlightedCells.length - 1) {
        // First click or reached the end, go to the first highlighted cell
        currentIndex = 0;
      } else {
        // Second click, go to the next highlighted cell
        currentIndex++;
      }

      // Scroll to the highlighted cell
      highlightedCells[currentIndex].scrollIntoView({ behavior: 'smooth' });
    }
  });

  // Find all the highlighted cells
  var arbitrageCells = document.querySelectorAll('td.arbitrage');
  arbitrageCells.forEach(function(cell) {
    var arbitrage = parseFloat(cell.textContent);
    if ((arbitrage >= 1 && arbitrage <= 20) || (arbitrage >= -20 && arbitrage <= -1)) {
      highlightedCells.push(cell);
    }
  });

  // Add the highlight class to the first highlighted cell
  if (highlightedCells.length > 0) {
    highlightedCells[0].classList.add('highlight');
  }
});


window.addEventListener('DOMContentLoaded', function() {
  var arrow = document.createElement('div');
  arrow.className = 'floating-arrow';
  document.body.appendChild(arrow);

  var highlightedCells = [];
  var currentIndex = -1;

  z

  // Find all the highlighted cells
  var arbitrageCells = document.querySelectorAll('td.arbitrage');
  arbitrageCells.forEach(function(cell) {
    var arbitrage = parseFloat(cell.textContent);
    if ((arbitrage >= 1 && arbitrage <= 20) || (arbitrage >= -20 && arbitrage <= -1)) {
      highlightedCells.push(cell);
      cell.classList.add('highlight');
    }
  });

  // Add the highlight class to the first highlighted cell
  if (highlightedCells.length > 0) {
    highlightedCells[0].classList.add('active');
  }
});

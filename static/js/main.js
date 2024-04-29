document.addEventListener('DOMContentLoaded', function() {
    const customSwitchInput = document.querySelector('#toggleButton');
    const consumableElements = document.querySelectorAll('.consumables');
  
    customSwitchInput.addEventListener('change', function() {
        consumableElements.forEach(function(element) {
            if (customSwitchInput.checked) {
              element.classList.remove('hidden');
            } else {
              element.classList.add('hidden');
            }
          });
    });
});


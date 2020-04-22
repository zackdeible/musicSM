$(window).on('load', function () {
  console.log('Hello world';)
  // initialization of autonomous popups
  $.HSCore.components.HSModalWindow.init('[data-modal-target]', '.js-modal-window', {
    autonomous: true
  });

  // initialization of clipboard
  $.HSCore.components.HSClipboard.init('.js-clipboard');
});

window.document.onload = () => {
  console.log('Hello World1');
}

window.onload = () => {
  console.log('Hello world');
}

function derp() {
  console.log('DERP');
}

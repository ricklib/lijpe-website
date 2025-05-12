window.addEventListener('mousemove', () => {
    const audio = document.getElementById('sfx1');
    audio.play();
}, { once: true });

window.addEventListener('click', () => {
    const audio = document.getElementById('sfx2');
    audio.play();
});
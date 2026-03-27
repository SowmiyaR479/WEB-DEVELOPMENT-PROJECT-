const robot = document.querySelector('.robot');
const danceButton = document.querySelector('.dance-button');
const stopButton = document.querySelector('.stop-button');

let isDancing = false;

function startDance() {
    if (!isDancing) {
        isDancing = true;
        robot.classList.add('dancing');

        document.querySelectorAll('.arm, .leg').forEach(function(el) {
            el.style.animationPlayState = 'running';
        });
    }
}

function stopDance() {
    if (isDancing) {
        isDancing = false;
        robot.classList.remove('dancing');

        document.querySelectorAll('.arm, .leg').forEach(function(el) {
            el.style.animationPlayState = 'paused';
        });
    }
}

danceButton.addEventListener('click', startDance);
stopButton.addEventListener('click', stopDance);

document.querySelectorAll('.arm, .leg').forEach(function(el) {
    el.style.animationPlayState = 'paused';
});
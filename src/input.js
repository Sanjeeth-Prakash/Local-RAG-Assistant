export class Input {
  constructor(canvas, game) {
    this.game = game;
    this.onAction = () => game.handleAction();
    this.onToggleMute = () => game.audio.toggle();

    const trigger = (e) => {
      e.preventDefault();
      this.onAction();
    };

    canvas.addEventListener('pointerdown', trigger);
    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space' || e.code === 'ArrowUp') {
        if (e.repeat) return;
        e.preventDefault();
        this.onAction();
      } else if (e.code === 'KeyM') {
        this.onToggleMute();
      } else if (e.code === 'Enter') {
        this.onAction();
      }
    });
  }
}

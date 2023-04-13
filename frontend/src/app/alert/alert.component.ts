import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-alert',
  templateUrl: './alert.component.html',
  styleUrls: ['./alert.component.sass'],
})
export class AlertComponent {

  @Input() type: string;
  @Input() message: string;

  @Output() closed = new EventEmitter();

  close() {
    this.closed.emit(false);
  }
}

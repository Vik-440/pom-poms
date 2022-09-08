import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-alert',
  templateUrl: './alert.component.html',
  styleUrls: ['./alert.component.sass']
})
export class AlertComponent implements OnInit {

  constructor() { }

  @Input() type: string;
  @Input() message: string;

  @Output() closed = new EventEmitter();
  ngOnInit(): void {
  }

  close() {
    this.closed.emit(false);
  }
 }

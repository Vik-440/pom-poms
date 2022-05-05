import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-reserve',
  templateUrl: './reserve.component.html',
  styleUrls: ['./reserve.component.sass']
})
export class ReserveComponent implements OnInit {

  constructor() { }

  reserveItems = [{
    id_color: 1,
    name_color: 'dd',
    width_color: 12,
    bab_quantity_color: 6,
    weight_color: 3045,
    model: 1,
    pars: 30
  }];
  ngOnInit(): void {
  }

}

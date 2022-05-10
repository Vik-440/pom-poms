import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-finances',
  templateUrl: './finances.component.html',
  styleUrls: ['./finances.component.sass']
})
export class FinancesComponent implements OnInit {

  constructor() { }

  items = [];
  
  ngOnInit(): void {
  }

}

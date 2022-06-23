import { Component, OnInit } from '@angular/core';
import { FinancesPageService } from '../services/finances.service';

@Component({
  selector: 'app-finances',
  templateUrl: './finances.component.html',
  styleUrls: ['./finances.component.sass']
})
export class FinancesComponent implements OnInit {

  constructor(private service: FinancesPageService) { }

  items = [];
  
  ngOnInit(): void {
    this.service.getFinances().subscribe()
  }

}

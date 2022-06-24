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
  methods;
  mainItems;
  outlayData;
  ngOnInit(): void {
    this.service.getFinances().subscribe((data: any) => {
      const copyData = data.slice(0);
      this.methods = data[0];
      this.outlayData = data[data.length - 1];
      this.mainItems = copyData.slice(1, data.length - 1);
      console.log(this.mainItems, copyData);
      
    })
  }

}

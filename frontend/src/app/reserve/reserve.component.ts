import { Component, OnInit } from '@angular/core';
import { MaterialPageService } from '../services/materials.service';

@Component({
  selector: 'app-reserve',
  templateUrl: './reserve.component.html',
  styleUrls: ['./reserve.component.sass']
})
export class ReserveComponent implements OnInit {

  constructor(private servieMaterial: MaterialPageService) { }

  reserveItems;
  ngOnInit(): void {
    this.servieMaterial.getListMaterial().subscribe(data => {
      this.reserveItems = data;
    });
  }

}

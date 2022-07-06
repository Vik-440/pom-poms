import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { switchMap } from 'rxjs';
import { MaterialPageService } from '../services/materials.service';

@Component({
  selector: 'app-reserve',
  templateUrl: './reserve.component.html',
  styleUrls: ['./reserve.component.sass']
})
export class ReserveComponent implements OnInit {

  constructor(private servieMaterial: MaterialPageService, private fb: FormBuilder) { }
  materialFilter = [];
  reverseItemData: FormGroup;
  reserveItems;
  reverseItemsCorrect = this.fb.array([]);
  idEdit = null;
  isNewMaterial = false;
  idChange = [];
  isHideOk = true;
  ngOnInit(): void {
    this.servieMaterial.getListMaterial().subscribe((data: any) => {
      this.reserveItems = data.sort((a,b) => a.name_color - b.name_color);
      
      this.reserveItems.map(item => {

        this.reverseItemsCorrect.push(this.fb.group({
          bab_quantity_color: null,
          weight_color: null
        }))
        
      })
    });

    this.materialFilter = [
      { id: 999, value: true, name: 'всі матеріали' },
      { id: null, value: false, name: 'матеріали в наявності' },
    ];

    this.reverseItemData = this.fb.group({
      id_color: '',
      name_color: ['', Validators.required],
      width_color: ['', Validators.required],
      thickness_color: ['', Validators.required],
      manufacturer_color: ['', Validators.required],
      bab_weight_color: '',
      weight_10m_color: ['', Validators.required],
      reserve_color: ['', Validators.required],
      bab_quantity_color: ['', Validators.required],
      weight_color: ['', Validators.required],
      comment_color: ''
    })
  }

  editItem(id) {
    this.idEdit = id;
    this.isNewMaterial = false;
    this.servieMaterial.getFullInfoMaterial(id).subscribe((data: any) => {
      this.reverseItemData.patchValue({
        id_color: data.id_color,
        name_color: data.name_color,
        width_color: data.width_color,
        thickness_color: data.thickness_color,
        manufacturer_color: data.manufacturer_color,
        bab_weight_color: data.bab_weight_color,
        weight_10m_color: data.weight_10m_color,
        reserve_color: data.reserve_color,
        bab_quantity_color: data.bab_quantity_color,
        weight_color: data.weight_color,
        comment_color: data.comment_color
      })
    })
  }

  createMaterial() {
    this.idEdit = null;
    this.isNewMaterial = true;
    this.reverseItemData.reset();
  }

  saveMaterial() {
    this.idEdit = null;
    let params = {
      ...this.reverseItemData.value
    };

    delete params['id_color'];
    if(this.isNewMaterial) {
      params = {
        ...params,
        color_new: 0
      }
    } else {
      params = {
        ...params,
        color_change_full: this.reverseItemData.value.id_color
      }
    }

    this.servieMaterial.saveMaterial(params).subscribe(() => {
      this.servieMaterial.getListMaterial().subscribe(data => {
        this.reserveItems = data;
        this.reverseItemData.reset();
      });
    });
  }

  filterMaterials(event) {
    if(event) {
      if(event.id) {
        this.servieMaterial.getFullAllMaterial({ id_color: 999}).subscribe((data: any) => {
          this.reserveItems =  data.sort((a,b) => a.name_color - b.name_color);;
        })
      } else {
        this.servieMaterial.getListMaterial().subscribe((data: any) => {
          this.reserveItems =  data.sort((a,b) => a.name_color - b.name_color);;
        });
      }
    }
    
  }

  changeMaterial(item, value, field, id) {
    this.idChange.push(id);
    this.isHideOk = false;
    item.patchValue({
      [field]: value
    });
  }

  saveChangesMat(id, item) {    
    const params = {
      color_change: id,
      bab_quantity_color: +item.value.bab_quantity_color,
      weight_color: +item.value.weight_color
    };
    this.servieMaterial.saveMaterial(params).pipe(
      switchMap(() => this.servieMaterial.getListMaterial())
    ).subscribe((data: any) => {
      this.idChange = this.idChange.filter(i => i !== id);
      this.reserveItems =  data.sort((a,b) => a.name_color - b.name_color);;
      item.reset();
    });
  }
}

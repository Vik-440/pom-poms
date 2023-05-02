import { Component, HostListener, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { switchMap } from 'rxjs';
import { MaterialPageService } from '../services/materials.service';

@Component({
  selector: 'app-reserve',
  templateUrl: './reserve.component.html',
  styleUrls: ['./reserve.component.sass'],
})
export class ReserveComponent implements OnInit {
  constructor(private _serviceMaterial: MaterialPageService, private _fb: FormBuilder) {}
  materialFilter = [];
  reverseItemData: FormGroup;
  reserveItems;
  reverseItemsCorrect = this._fb.array([]);
  idEdit = null;
  isNewMaterial = true;
  idChange = [];
  isHideOk = true;
  filterMaterial = null;
  isShowSpinner = false;
  alert = {
    type: '',
    message: '',
    isShow: false,
  };
  @ViewChild('blockEdit', { static: true }) blockEdit;
  @HostListener('window:scroll', ['$event']) // for window scroll events
  onScroll() {
    this.blockEdit.nativeElement.setAttribute('style', `top: ${window.scrollY}px`);
  }

  ngOnInit(): void {
    this.getMaterialList();
    this.materialFilter = [
      { value: 'all', name: 'всі матеріали' },
      { value: null, name: 'матеріали в наявності' },
    ];
    this.reverseItemData = this._fb.group({
      id_material: '',
      name: ['', Validators.required],
      width: [null, Validators.required],
      thickness: [null, Validators.required],
      manufacturer: ['', Validators.required],
      spool_weight: null,
      weight_10m: [null, Validators.required],
      reserve: [null, Validators.required],
      spool_qty: [null, Validators.required],
      weight: [null, Validators.required],
      comment: '',
    });
  }

  getMaterialList() {
    this._serviceMaterial.getListMaterial().subscribe(
      (data: any) => {
        this.prepareListMaterial(data);
      },
      () => {}
    );
  }

  prepareListMaterial(data) {
    this.reserveItems = data.sort((a, b) => a.name - b.name);
    this.reserveItems.map(() => {
      this.reverseItemsCorrect.push(
        this._fb.group({
          edit_spool_qty: null,
          edit_weight: null,
        })
      );
    });
  }

  editItem(id) {
    this._serviceMaterial.getFullInfoMaterial(id).subscribe((data: any) => {
      this.idEdit = id;
      this.isNewMaterial = false;
      this.reverseItemData.patchValue({
        id_material: data.id_material,
        name: data.name,
        width: data.width,
        thickness: data.thickness,
        manufacturer: data.manufacturer,
        spool_weight: data.spool_weight,
        weight_10m: data.weight_10m,
        reserve: data.reserve,
        spool_qty: data.spool_qty,
        weight: data.weight,
        comment: data.comment,
      });
    }, () => {
        this.showAlert('danger', 'Щось не так');
    });
  }

  createMaterial() {
    this.idEdit = null;
    this.isNewMaterial = true;
    this.reverseItemData.reset();
  }

  saveMaterial() {
    this.idEdit = null;
    const params = {
      ...this.reverseItemData.value,
    };
    this.isShowSpinner = true;
    this._serviceMaterial
      .saveMaterial(params)
      .pipe(
        switchMap(() => {
          return this._serviceMaterial.getListMaterial();
        })
      )
      .subscribe(
        (data: any[]) => {
          this.isShowSpinner = false;
          this.isShowSpinner = false;
          this.prepareListMaterial(data);
          this.reverseItemData.reset();
        },
        () => {
          this.isShowSpinner = false;
        }
      );
  }

  editMaterial() {
    const params = {
      ...this.reverseItemData.value,
    };
    delete params.id_material;
    this.isShowSpinner = true;
    this._serviceMaterial
      .editMaterial(params, this.reverseItemData.value.id_material)
      .pipe(
        switchMap(() => {
          return this._serviceMaterial.getListMaterial();
        })
      )
      .subscribe(
        (data: any[]) => {
          this.isShowSpinner = false;
          this.prepareListMaterial(data);
          this.isShowSpinner = false;
          this.reverseItemData.reset();
        },
        () => {
          this.isShowSpinner = false;
        }
      );
  }
  getMaterialByFilter() {
    this.isShowSpinner = true;
    this._serviceMaterial.getListMaterial(this.filterMaterial ? { available: this.filterMaterial } : {}).subscribe(
      (data: any) => {
        this.prepareListMaterial(data);
        this.isShowSpinner = false;
      },
      (err) => {
        this.isShowSpinner = false;
        this.reserveItems = [];
        this.showAlert('danger', err.error.materials);
      }
    );
  }

  calculateMat(form) {
    form.patchValue({
      weight: this.calculateWeight(form.value.weight),
    });
  }

  calculateWeight(value) {
    let total = 0;
    value = value.toString().match(/[+\-]*(\.\d+|\d+(\.\d+)?)/g) || [];
    while (value.length) {
      total += parseFloat(value.shift());
    }
    return total;
  }

  changeMaterial(item, value, field, id) {
    this.idChange.push(id);
    this.isHideOk = false;
    item.patchValue({
      [field]: +value,
    });
  }

  saveChangesMat(id, item) {
    this.isShowSpinner = true;
    this._serviceMaterial.saveConsumptionMaterial(item.value, id).subscribe(
      (data: any) => {
        this.isShowSpinner = false;
        this.idChange = this.idChange.filter((i) => i !== id);
        this.reserveItems.forEach((item) => {
          if (item.id_material === id) {
            item.net_weight = data.net_weight;
            item.spool_qty = data.spool_qty;
          }
        });
        this.reverseItemData.patchValue({
          edit_spool_qty: this.reverseItemData.value.edit_spool_qty + item.value.edit_spool_qty,
          edit_weight: this.reverseItemData.value.edit_weight + item.value.edit_weight,
        });
        this.isShowSpinner = false;

        this.showAlert('success',  'Дані збережено');
        item.reset();
      },
      () => {
        this.isShowSpinner = false;
        this.showAlert('danger', 'Уппс, щось пішло не так');
      }
    );
  }

  showAlert(type, message) {
    this.alert = {
        isShow: true,
        type: type,
        message: message,
      };
      setTimeout(() => {
        this.alertChange(false);
      }, 3000);
  }

  alertChange(e) {
    this.alert.isShow = e;
  }
}

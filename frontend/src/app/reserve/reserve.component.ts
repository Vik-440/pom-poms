import { Component, HostListener, OnInit, QueryList, ViewChild, ViewChildren } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MaterialPageService } from '../services/materials.service';
import { NgbTooltip } from '@ng-bootstrap/ng-bootstrap';
import { calculateString } from '../utils/calcstring';
import { interval, takeWhile } from 'rxjs';
import { AlertInterface } from '../interfaces/alert';
import { ConsumptionDataInterface, MaterialFormInterface, MaterialsItemInterface } from '../interfaces/materials';

@Component({
  selector: 'app-reserve',
  templateUrl: './reserve.component.html',
  styleUrls: ['./reserve.component.sass'],
})
export class ReserveComponent implements OnInit {
  constructor(private _serviceMaterial: MaterialPageService, private _fb: FormBuilder) {}

  materials: MaterialsItemInterface[] = [];
  availabilityFilters = [
    {
      value: 'всі матеріали',
      key: 'all',
    },
    {
      value: 'матеріали в наявності',
      key: null,
    },
  ];
  availabilityData: string | null;
  materialForm: FormGroup;
  isNewMaterial: boolean = true;
  isShowOk: boolean = false;
  idChangeMaterial: number;
  isShowJustMaterial: boolean = false;
  intervalShowTooltip;
  isShowTooltip: boolean = false;
  idEditMaterial: number;
  isShowSpinner: boolean = false;
  alert = {
    isShow: false,
    type: '',
    message: '',
  };

  @ViewChildren('tooltipElementWeight') tooltipElementWeight: QueryList<NgbTooltip>;
  @ViewChildren('tooltipElementQty') tooltipElementQty: QueryList<NgbTooltip>;
  @ViewChild('blockEdit', { static: true }) blockEdit;
  @HostListener('window:scroll', ['$event'])
  onScroll() {
    this.blockEdit.nativeElement.setAttribute('style', `top: ${window.scrollY || 150}px; bottom: ${50}px`);
  }

  ngOnInit(): void {
    this.getAllMaterials();
    this.createMaterialForm();
  }

  getAllMaterials() {
    this.isShowSpinner = true;
    this._serviceMaterial.getListMaterial().subscribe((data: MaterialsItemInterface[]) => {
      this.prepareMaterial(data);
      this.isShowSpinner = false;
      this.showMessageAlert({
        isShow: true,
        type: 'success',
        message: 'Дані завантажено',
      });
    });
  }

  getNumberMaterial(name: string) {
    if (name.includes('/') || name.includes('-')) {
      const result = name.split('/')[0];
      return result.length === name.length ? name.split('-')[0] : result;
    }
    return name;
  }

  createMaterialForm() {
    this.materialForm = this._fb.group({
      comment: '',
      id_material: null,
      manufacturer: '',
      name: '',
      reserve: null,
      spool_qty: null,
      spool_weight: null,
      thickness: null,
      weight: null,
      weight_10m: null,
      width: null,
    });
  }

  changesMaterialForm() {
    this.materialForm.valueChanges.subscribe(() => {
      this.isShowJustMaterial = false;

      this.isNewMaterial = false;
        // this.isShowJustMaterial = true;
    });
  }

  prepareMaterial(data) {
    this.materials = data
      .map((material) => {
        material.edit_spool_qty = null;
        material.edit_weight = null;
        return material;
      })
      .sort((one, two) => (one.name > two.name ? 1 : -1));
  }

  getMaterialByFilter() {
    this.isShowSpinner = true;
    this._serviceMaterial
      .getListMaterial(
        this.availabilityData
          ? {
              available: this.availabilityData,
            }
          : {}
      )
      .subscribe((data: MaterialsItemInterface[]) => {
        this.isShowSpinner = false;
        this.prepareMaterial(data);
        this.showMessageAlert({
          isShow: true,
          type: 'success',
          message: 'Дані завантажено',
        });
      });
  }

  openMaterial(id: number) {
    this.idEditMaterial = id;
    this._serviceMaterial.getFullInfoMaterial(id).subscribe((data: MaterialFormInterface) => {
      this.materialForm = this._fb.group({
        ...data,
      });
      this.isNewMaterial = false;
      this.isShowJustMaterial = true;
      this.changesMaterialForm();
    });
  }

  startCreateMaterial() {
    this.createMaterialForm();
    this.isNewMaterial = true;
    this.idEditMaterial = null;
    this.isShowJustMaterial = false;
  }

  changeMaterial(item, value, field, id, index) {
    const arrayTooltips = field === 'edit_weight' ? this.tooltipElementWeight.toArray() : this.tooltipElementQty.toArray();
    const regex = /[+\-*/]/g;
    const matches = value.match(regex);
    arrayTooltips[index].close();
    if (Number.isNaN(+value) && matches) {
      arrayTooltips[index].ngbTooltip = Number.isNaN(calculateString(value)) ? '' : String(calculateString(value));
      this.isShowTooltip = true;
      interval(500)
        .pipe(takeWhile(() => this.isShowTooltip))
        .subscribe(() => {
          arrayTooltips[index].open();
        });
      this.isShowOk = false;
    } else if (!Number.isNaN(+value)) {
      item[field] = value;
      arrayTooltips[index].ngbTooltip = value;
      const valid =
        (String(item.edit_weight).length && !Number.isNaN(+item.edit_weight)) ||
        (String(item.edit_spool_qty).length && !Number.isNaN(+item.edit_spool_qty));
      this.isShowOk = valid && !Number.isNaN(+value) ? true : false;
    }
    this.idChangeMaterial = id;
  }

  saveChangedMaterial(material, field, target, index) {
    const value = target.value;
    target.blur();
    material[field] = calculateString(value);
    this.isShowTooltip = false;
    this.isShowOk = true;
    field === 'edit_weight' ? this.tooltipElementWeight.toArray()[index].close() : this.tooltipElementQty.toArray()[index].close();
  }

  clearChangesMaterials() {
    this.isShowTooltip = false;
  }

  saveChangesMaterial(material: MaterialsItemInterface) {
    this._serviceMaterial
      .saveConsumptionMaterial(
        {
          edit_spool_qty: +material.edit_spool_qty,
          edit_weight: +material.edit_weight,
        },
        material.id_material
      )
      .subscribe((data: ConsumptionDataInterface) => {
        material.net_weight = data.net_weight;
        material.spool_qty = data.spool_qty;
        material.edit_spool_qty = null;
        material.edit_weight = null;
        this.isShowOk = false;
        this.showMessageAlert({
          isShow: true,
          type: 'success',
          message: 'Дані збережено',
        });
      });
  }

  gerParamsForSaveMaterial() {
    const params = {
      ...this.materialForm.value,
    };
    delete params.id_material;
    return params;
  }

  saveMaterial() {
    this._serviceMaterial.saveMaterial(this.gerParamsForSaveMaterial()).subscribe(
      (data: any) => {
        this.showMessageAlert({
          isShow: true,
          type: 'success',
          message: 'Матеріал збережено',
        });
        this.materialForm.patchValue({
          id_material: data.id_material,
        });
        this.idEditMaterial = data.id_material;
        this.getAllMaterials();
        this.isNewMaterial = false;
        this.isShowJustMaterial = true;
        this.changesMaterialForm();
      },
      ({ error }) => {
        this.materialForm.setErrors(error);
        this.showMessageAlert({
          isShow: true,
          type: 'danger',
          message: 'Щось пішло не так',
        });
      }
    );
  }

  editMaterial() {
    this._serviceMaterial.editMaterial(this.gerParamsForSaveMaterial(), this.materialForm.value.id_material).subscribe((data: any) => {
      this.showMessageAlert({
        isShow: true,
        type: 'success',
        message: 'Матеріал збережено',
      });
      this.materials.forEach((material: MaterialsItemInterface) => {
        if (material.id_material === data.edit_material) {
          material.width = this.materialForm.value.width;
          material.spool_qty = this.materialForm.value.spool_qty;
          material.net_weight = this.materialForm.value.weight - this.materialForm.value.spool_weight * this.materialForm.value.spool_qty;
        }
      });
    });
  }

  showMessageAlert(alert: AlertInterface) {
    this.alert = {
      isShow: alert.isShow,
      type: alert.type,
      message: alert.message,
    };
    setTimeout(() => {
      this.alert.isShow = false;
    }, 3000);
  }
}

import { Component, OnInit } from '@angular/core';
import { SettingsService } from '../services/settings.service';
import { modelsData } from '../utils/modelsData';
import { forkJoin, switchMap } from 'rxjs';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.sass'],
})
export class SettingsComponent implements OnInit {
  constructor(private _settingsService: SettingsService, private _fb: FormBuilder) {}

  modelsType = modelsData;
  Object = Object;
  defaultWeekdays = [1, 4];
  weekDays = [
    {
      label: 'Понеділок',
      id: 1,
    },
    {
      label: 'Вівторок',
      id: 2,
    },
    {
      label: 'Середа',
      id: 3,
    },
    {
      label: 'Четвер',
      id: 4,
    },
    {
      label: 'П\'ятниця',
      id: 5,
    },
    {
      label: 'Субота',
      id: 6,
    },
    {
      label: 'Неділя',
      id: 7,
    },
  ];

  params: string[] = [];
  paramsInfo: any;
  isAddNewModel = false;
  newModel: FormGroup;
  dates: moment.Moment[] = []
  public dateValues: Date[] = [new Date('1/12/2023'), new Date('1/15/2023'), new Date('1/3/2023'), new Date('1/25/2023')];
  ngOnInit(): void {
    this._settingsService.getAppSettings().pipe(
      switchMap((data: string[]) => {
        this.params = data;
        const arraysParams = [];
        this.params.forEach((param) => arraysParams.push(this._settingsService.getInfoAboutAppSetting(param)));
        return forkJoin(arraysParams);
      })
    ).subscribe((info) => {
      let a = [];
      info.forEach(i => {
        a = {
          ...a,
          ...i,
        }
      })
      this.paramsInfo = a;
      this.modifySettings();
    });
  }

  modifySettings() {
    this.params.forEach((param: string) => {
      this.paramsInfo[param].parameter_str = JSON.parse(this.paramsInfo[param].parameter_str);
    });

    console.log(this.paramsInfo)
  }

  createSettings(setting, value) {
    console.log(setting, value.value)
    this._settingsService.createAppSetting({
      parameter_description: 'Моделі',
      'parameter_name': setting,
      'parameter_int': 0,
      'parameter_str': JSON.stringify([]),
    }).subscribe(() => {
      this.paramsInfo = {
        ...this.paramsInfo,
        [setting]: {
          parameter_description: 'Моделі',
          'parameter_name': setting,
          'parameter_int': 0,
          'parameter_str': '',
        },
      }

      console.log(this.paramsInfo)
    })
  }

  isSelected = (event: any) => {
    const date = event as moment.Moment
    
    return (this.dates.find(x => x.isSame(date))) ? 'selected' : null;
  };
  
  select(event: any, calendar: any) {
    // const date: moment.Moment = event

    // const index = this.dates.findIndex(x => x?.isSame(date));
    // if (index < 0) this.dates.push(date);
    // else this.dates.splice(index, 1);

    calendar.updateTodaysDate();
  }
  updateSetting(setting) {
    if (setting === 'modelsData') {
      this.paramsInfo[setting].parameter_str = {
        ...this.paramsInfo[setting].parameter_str,
        [this.newModel.value.id]: this.newModel.value.type.toString(),
      }

      this._settingsService.updateAppSetting(setting, this.paramsInfo[setting]).subscribe(() => {
        this.isAddNewModel = false;
        this.newModel.reset();
      });
      return;
    }
    this._settingsService.updateAppSetting(setting, this.paramsInfo[setting]).subscribe();
  }

  deleteModel(key) {
    delete this.paramsInfo.modelsData.parameter_str[key]
    this._settingsService.updateAppSetting('modelsData', this.paramsInfo.modelsData).subscribe();
  }

  addMaterial() {
    this.isAddNewModel = true;
    this.newModel = this._fb.group({
      id: [null, Validators.required],
      type: [null, Validators.required],
    });
    console.log(this.newModel)
  }
}

import { Component, OnInit } from '@angular/core';
import { MainPageService } from '../services/main-table.service';

@Component({
    selector: 'app-main-table',
    templateUrl: './main-table.component.html',
    styleUrls: ['./main-table.component.sass'],
})
export class MainTableComponent implements OnInit {
    orders = [];
    isShowSpinner = false;
    constructor(private service: MainPageService) {}

    ngOnInit(): void {
        this.getAllData();
    }

    getAllData() {
        this.isShowSpinner = true;
        this.service.getListMain().subscribe(
            (data: any) => {
                this.orders = data;
                this.isShowSpinner = false;
            },
            () => {
                this.isShowSpinner = false;
            }
        );
    }

    getSumPhases(phase) {
        let sum = 0;
        this.orders.map((item) => {
            if (!item.fulfilled_order) {
                sum += Array.isArray(item[phase])
                    ? item[phase].reduce((partialSum, a) => partialSum + a, 0)
                    : item[phase];
            }
        });
        return sum;
    }

    isArray(array) {
        return Array.isArray(array);
    }

    getColorForMoney(order) {
        const interest = (100 * order.real_money) / order.sum_payment;
        if (interest < 10) {
            return 'red';
        } else if (interest >= 100) {
            return 'green';
        }
    }

    getMoney(sum) {
        return Number(sum).toFixed(sum.toString().endsWith('.00') ? null : 2);
    }

    isHasCity(city) {
        return city.includes('самовивіз');
    }

    tooltipCity(order) {
        const regexPhone = /(\d{2})(\d{3})(\d{3})(\d{2})(\d{2})/g;
        const tooltip = [
            'Н.П. №' + order.np_number,
            order.first_name_client + ' ' + order.second_name_client,
            order.phone_recipient.replace(regexPhone, '$1-' + '$2-' + '$3-' + '$4-' + '$5'),
            order.zip_code,
            order.street_house_apartment,
        ];
        return tooltip.filter((data) => data).join('\n');
    }

    changeHeight(j, i) {
      return {
          height: `${document.querySelectorAll(`#kolorModel-${j}-${i}`)[0].clientHeight}px`,
      };
  }

  checkCode(kodModel, commentModel) {
    if (commentModel) {
        return 'yellow';
    }
    const letterModel = kodModel.split('');
    if (+letterModel[2] !== 0) {
        return 'light-pink';
    }
    const splitModelH = kodModel.split('-');
    if (splitModelH[1]?.split('')[0] === 'В' || splitModelH[1]?.split('')[0] === 'B') {
        return 'light-blue';
    }

    return '';
}
}

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { TableComponent, SortDirective } from './table/table.component';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from './navbar/navbar.component';
import { environment } from 'src/environments/environment';
import { TooltipModule, TooltipOptions } from '@teamhive/ngx-tooltip';
import { CreateOrderComponent } from './create-order/create-order.component';
import { NgToggleModule } from 'ngx-toggle-button';
import { DatepickerModule } from 'ng2-datepicker';
import { MyDatePickerModule } from 'mydatepicker';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ReserveComponent } from './reserve/reserve.component';
import { NgSelectModule } from '@ng-select/ng-select';


@NgModule({
  declarations: [
    AppComponent,
    SortDirective,
    TableComponent,
    NavbarComponent,
    CreateOrderComponent,
    ReserveComponent
  ],
  imports: [
    NgToggleModule,
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgbModule,
    CommonModule,
    DatepickerModule,
    FormsModule,
    NgSelectModule,
    ReactiveFormsModule,
    TooltipModule.forRoot({
        placement: 'top',
        arrow: 'true',
        arrowType: 'sharp',
        allowHTML: true,
        maxWidth: 200
      } as unknown as TooltipOptions)
  ],
  providers: [
    { provide: 'API_URL', useValue: environment.apiUrl }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

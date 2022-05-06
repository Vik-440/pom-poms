import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreateOrderComponent } from './create-order/create-order.component';
import { FinancesComponent } from './finances/finances.component';
import { ReserveComponent } from './reserve/reserve.component';
import { TableComponent } from './table/table.component';

const routes: Routes = [
  { path: 'base-page', component: TableComponent },
  { path: 'create-order', component: CreateOrderComponent },
  { path: 'reserve-page', component: ReserveComponent },
  { path: 'finances-page', component: FinancesComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

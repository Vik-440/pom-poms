import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreateOrderComponent } from './create-order/create-order.component';
import { FinancesComponent } from './finances/finances.component';
import { ReserveComponent } from './reserve/reserve.component';
import { TableComponent } from './table/table.component';

const routes: Routes = [
  { path: '', component: TableComponent },
  { path: 'create-order', component: CreateOrderComponent },
  { path: 'materials', component: ReserveComponent },
  { path: 'finances-page', component: FinancesComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { onSameUrlNavigation: 'reload' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }

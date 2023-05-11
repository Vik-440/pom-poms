export interface MaterialsItemInterface {
  id_material: number;
  name: string;
  net_weight: number;
  spool_qty: number;
  width: number;
  edit_spool_qty?: number;
  edit_weight?: number;
}

export interface MaterialFormInterface {
  comment: string;
  id_material: number;
  manufacturer: string;
  name: string;
  reserve: number;
  spool_qty: number;
  spool_weight: number;
  thickness: number;
  weight: number;
  weight_10m: number;
  width: number;
}

export interface ConsumptionDataInterface {
  spool_qty: number;
  net_weight: number;
}
export interface AlertInterface {
  isShow: boolean;
  type: 'success' | 'info' | 'warning' | 'danger' | 'primary' | 'secondary' | 'light' | 'dark';
  message: string;
}
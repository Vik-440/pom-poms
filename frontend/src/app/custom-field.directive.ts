import { Directive, ElementRef } from '@angular/core';

@Directive({
  selector: '[appCustomField]'
})
export class CustomFieldDirective {

  constructor(private el: ElementRef) { }

}

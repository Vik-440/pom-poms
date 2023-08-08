import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NovePoshtaModalComponent } from './nove-poshta-modal.component';

describe('NovePoshtaModalComponent', () => {
  let component: NovePoshtaModalComponent;
  let fixture: ComponentFixture<NovePoshtaModalComponent>;

  beforeEach(async() => {
    await TestBed.configureTestingModule({
      declarations: [ NovePoshtaModalComponent ],
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NovePoshtaModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

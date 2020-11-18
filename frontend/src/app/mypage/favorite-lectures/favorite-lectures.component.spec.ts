import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FavoriteLecturesComponent } from './favorite-lectures.component';

describe('FavoriteLecturesComponent', () => {
  let component: FavoriteLecturesComponent;
  let fixture: ComponentFixture<FavoriteLecturesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FavoriteLecturesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FavoriteLecturesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

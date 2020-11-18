import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FavoriteSitesComponent } from './favorite-sites.component';

describe('FavoriteSitesComponent', () => {
  let component: FavoriteSitesComponent;
  let fixture: ComponentFixture<FavoriteSitesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FavoriteSitesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FavoriteSitesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

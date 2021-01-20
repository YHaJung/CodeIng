import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { FavoriteSitesComponent } from './favorite-sites.component';

describe('FavoriteSitesComponent', () => {
  let component: FavoriteSitesComponent;
  let fixture: ComponentFixture<FavoriteSitesComponent>;

  beforeEach(waitForAsync(() => {
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

import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MypageSpecificComponent } from './mypage-specific.component';

describe('MypageSpecificComponent', () => {
  let component: MypageSpecificComponent;
  let fixture: ComponentFixture<MypageSpecificComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MypageSpecificComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MypageSpecificComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

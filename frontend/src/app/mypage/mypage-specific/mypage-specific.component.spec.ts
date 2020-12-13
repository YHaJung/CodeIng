import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { MypageSpecificComponent } from './mypage-specific.component';

describe('MypageSpecificComponent', () => {
  let component: MypageSpecificComponent;
  let fixture: ComponentFixture<MypageSpecificComponent>;

  beforeEach(waitForAsync(() => {
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

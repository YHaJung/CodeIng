import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { LectureCardMiddleComponent } from './lecture-card-middle.component';

describe('LectureCardMiddleComponent', () => {
  let component: LectureCardMiddleComponent;
  let fixture: ComponentFixture<LectureCardMiddleComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureCardMiddleComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureCardMiddleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

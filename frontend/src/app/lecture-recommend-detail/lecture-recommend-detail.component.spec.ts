import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { LectureRecommendDetailComponent } from './lecture-recommend-detail.component';

describe('LectureRecommendDetailComponent', () => {
  let component: LectureRecommendDetailComponent;
  let fixture: ComponentFixture<LectureRecommendDetailComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureRecommendDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureRecommendDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

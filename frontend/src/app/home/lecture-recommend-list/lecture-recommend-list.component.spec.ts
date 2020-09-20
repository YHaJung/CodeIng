import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LectureRecommendListComponent } from './lecture-recommend-list.component';

describe('LectureRecommendListComponent', () => {
  let component: LectureRecommendListComponent;
  let fixture: ComponentFixture<LectureRecommendListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureRecommendListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureRecommendListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

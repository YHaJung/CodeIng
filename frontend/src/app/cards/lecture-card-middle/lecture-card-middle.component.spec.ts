import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LectureCardMiddleComponent } from './lecture-card-middle.component';

describe('LectureCardMiddleComponent', () => {
  let component: LectureCardMiddleComponent;
  let fixture: ComponentFixture<LectureCardMiddleComponent>;

  beforeEach(async(() => {
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

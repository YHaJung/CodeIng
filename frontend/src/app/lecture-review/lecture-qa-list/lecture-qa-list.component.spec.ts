import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LectureQaListComponent } from './lecture-qa-list.component';

describe('LectureQaListComponent', () => {
  let component: LectureQaListComponent;
  let fixture: ComponentFixture<LectureQaListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureQaListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureQaListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

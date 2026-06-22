; ModuleID = "semantica"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"()
{
entry:
  %"a" = alloca i32
  %"b" = alloca i32
  %"c" = alloca i1
  store i32 1, i32* %"a"
  store i32 2, i32* %"b"
  %"a.1" = load i32, i32* %"a"
  %"b.1" = load i32, i32* %"b"
  %".4" = icmp sgt i32 %"a.1", %"b.1"
  br i1 %".4", label %"then", label %"else"
then:
  store i1 1, i1* %"c"
  br label %"merge"
else:
  store i1 0, i1* %"c"
  br label %"merge"
merge:
  ret i32 0
}
